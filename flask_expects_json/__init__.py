from functools import wraps
from flask import request, g, abort

from jsonschema import validate, ValidationError, FormatChecker
from .default_validator import ExtendedDefaultValidator


def expects_json(schema=None, force=False, fill_defaults=False, ignore_for=None):
    if schema is None:
        schema = dict()
    if ignore_for is not None:
        if isinstance(ignore_for, str):
            raise TypeError('Methods should be wrapped in an iterable. i.e. ignore_for=["GET"]')

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if ignore_for is not None and request.method in ignore_for:
                return f(*args, **kwargs)

            data = request.get_json(force=force)

            if data is None:
                return abort(400, 'Failed to decode JSON object')

            try:
                format_checker = FormatChecker()

                if fill_defaults:
                    ExtendedDefaultValidator(schema, format_checker=format_checker).validate(data)
                else:
                    validate(data, schema, format_checker=format_checker)
            except ValidationError as e:
                return abort(400, e)

            g.data = data
            return f(*args, **kwargs)
        return decorated_function
    return decorator
