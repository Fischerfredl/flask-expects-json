[![version](https://img.shields.io/pypi/v/flask-expects-json.svg)](https://pypi.python.org/pypi/flask-expects-json)
[![license](https://img.shields.io/pypi/l/flask-expects-json.svg)](https://pypi.python.org/pypi/flask-expects-json)
[![pyversions](https://img.shields.io/pypi/pyversions/flask-expects-json.svg)](https://pypi.python.org/pypi/flask-expects-json)
[![pipeline status](https://travis-ci.org/Fischerfredl/flask-expects-json.svg?branch=master)](https://travis-ci.org/Fischerfredl/flask-expects-json)
[![coverage](https://img.shields.io/codecov/c/github/fischerfredl/flask-expects-json.svg)](https://codecov.io/gh/Fischerfredl/flask-expects-json)

# flask-expects-json

Decorator for REST endpoints in flask. Validate JSON request data.

When building json REST services I find myself already specifying json-schema for POST data while defining swagger spec. This package brings json validation to flask. It omits the need to validate the data yourself while profiting from an already established standard (http://json-schema.org/). Defining the schema right before the route helps the self-documentation of an endpoint (see usage).


This package uses jsonschema to for validation: https://pypi.python.org/pypi/jsonschema

## Installation

Use pip to install the package from PyPI:

```bash
pip install flask-expects-json
```

If you are intending to install async version:

```bash
pip install flask-expects-json[async]
```
Note: the above command is not necessary in order to install a version
of flask-expect-json that supports async, however, the above command
will ensure `flask[async]` is installed as a dependency.

## Usage

This package provides a flask route decorator to validate json payload.

```python
from flask import Flask, jsonify, g, url_for
from flask_expects_json import expects_json
# example imports
from models import User
from orm import NotUniqueError

app = Flask(__name__)

schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'email': {'type': 'string'},
        'password': {'type': 'string'}
    },
    'required': ['email', 'password']
}


@app.route('/register', methods=['POST'])
@expects_json(schema)
def register():
    # if payload is invalid, request will be aborted with error code 400
    # if payload is valid it is stored in g.data

    # do something with your data
    user = User().from_dict(g.data)
    try:
        user.save()
    except NotUniqueError as e:
        # exception path: duplicate database entry
        return jsonify(dict(message=e.message)), 409

    # happy path: json response
    resp = jsonify(dict(auth_token=user.encode_auth_token(), user=user.to_dict()))
    resp.headers['Location'] = url_for('users.get_user', user_id=user.id)
    return resp, 201
```

The expected json payload is recognizable through "schema". If schema is not met the requests aborts (400) with a hinting error message.


## Mimetype checking

As of 1.2.0 this decorator uses `flask.request.get_json(force=False)` to get the data. This means the mimetype of the request has to be 'application/json'. Can be disabled by setting `force=False`. Be aware that this creates a major security vulnerability to CSRF since CORS is not enforced for certain mimetypes. Thanks to Argishti Rostamian for noticing.

```python
@app.route('/strict')
@expects_json()
def strict():
    return 'This view will return 400 if mimetype is not \'application/json\' 
    
@app.route('/insecure')
@expects_json({}, force=False)
def insecure():
    return 'This view will validate the data no matter the mimetype.'
```

## Format checking

As of 1.6.0 you can set `check_formats=True` or `check_formats=['list of format']` to enable validating formats such as `email` `date-time`. This is set to `False` by default.

## Default values

Normally validators wont touch the data. By default this package will not fill in missing default values provided in the schema. If you want to you can set `fill_defaults=True` explicitly. The validation will be performed after this action, so default values can lead to invalid data.

## Skip validation methods

If you want to skip the validation for certain HTTP methods, specify them with `ignore_for=[]`. Typical methods that do not expect a body are GET, HEAD and DELETE. Thanks to @mtheos for implementing this.

```python
@app.route('/', methods=['GET', 'POST'])
@expects_json(schema, ignore_for=['GET'])
def register():
    return 
```

## Error handling

On validation failure the library calls `flask.abort` and passes an 400 error code and the validation error.
By default this creates an HTML error page and displays the error message.
To customize the behavior use the error handling provided by flask ([docs](https://flask.palletsprojects.com/en/1.1.x/errorhandling/#error-handlers)).
This can be useful to e.g hide the validation message from users or provide a JSON response.

The original [ValidationError](https://python-jsonschema.readthedocs.io/en/latest/errors/#jsonschema.exceptions.ValidationError) is passed to `flask.abort`, which itself passes arguments to `werkzeug.exceptions.HTTPException` so it can be retrieved on `error.description` like this:

```python
from flask import make_response, jsonify
from jsonschema import ValidationError

@app.errorhandler(400)
def bad_request(error):
    if isinstance(error.description, ValidationError):
        original_error = error.description
        return make_response(jsonify({'error': original_error.message}), 400)
    # handle other "Bad Request"-errors
    return error
```

## Testing

The following are the steps to create a virtual environment into a folder named "venv" and install the requirements.

```bash
# Create virtualenv
python3 -m venv venv
# activate virtualenv
source venv/bin/activate
# update packages
pip install --upgrade pip setuptools wheel
# install requirements
python setup.py install
```

Tests can be run with `python setup.py test` when the virtualenv is active.

# Changelog

## Unreleased

## 1.7.0 - 2021-11-08
- Feature: support flask async (thanks @jiashuChen)

## 1.6.0 - 2021-08-09
- Feature: added optional format validation (thanks @CrafterSvK)

## 1.5.0 - 2020-08-24
- Feature: ignore validation for certain HTTP methods. (thanks @mtheos)

## 1.4.0 - 2019-09-02
- Updated dependencies to new major versions.
- Removed Python 3.4 support (as jsonschema did)
- Fixed: Typo in readme
- Changed: Pass whole error object to the 400 abort on schema validation error

## [1.3.1]
- Changed error message when get_json() fails. 
- Bugfix in DefaultValidatingDraft4Validator when trying to set a default value on strings.

## [1.3.0] - 2018-02-16
- Changed: Defaults wont be filled in request data by default. Set fill_defaults=True explicitly.

## [1.2.0] - 2018-02-15
- Security: set force=False as default argument for mimetype checking. Before: force=True for convenience

## [1.1.0] - 2018-02-03
- Added missing default values will be automatically filled into the request data
- Added parameter fill_defaults

## [1.0.6] - 2018-01-29
- Added tests for Python 3.4, 3.5, 3.6
- Added code coverage
- Changed code-style/readme. 

## 1.0.0 - 2018-01-21
- Added initial version of expects_json() decorator
- Added simple validation of request data
- Added store data in g.data

[Unreleased]: https://github.com/fischerfredl/flask-expects-json/compare/1.3.1...HEAD
[1.3.1]: https://github.com/fischerfredl/flask-expects-json/compare/1.2.0...1.3.1
[1.3.0]: https://github.com/fischerfredl/flask-expects-json/compare/1.2.0...1.3.0
[1.2.0]: https://github.com/fischerfredl/flask-expects-json/compare/1.1.0...1.2.0
[1.1.0]: https://github.com/fischerfredl/flask-expects-json/compare/1.0.6...1.1.0
[1.0.6]: https://github.com/fischerfredl/flask-expects-json/compare/1.0.0...1.0.6
