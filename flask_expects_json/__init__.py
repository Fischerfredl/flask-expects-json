from functools import wraps
from flask import request, g, abort

from jsonschema import validate, ValidationError


def expects_json(schema=None):
    if schema is None:
        schema = dict()

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json(force=True)

            try:
                validate(data, schema)
            except ValidationError as e:
                return abort(400, e.message)

            g.data = data
            return f(*args, **kwargs)
        return decorated_function
    return decorator
