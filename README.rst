|version| |license| |pyversions| |pipeline status| |coverage|

flask-expects-json
==================

Decorator for REST endpoints in flask. Validate JSON request data.

When building json REST services I find myself already specifying
json-schema for POST data while defining swagger spec. This package
brings json validation to flask. It omits the need to validate the data
yourself while profiting from an already established standard
(http://json-schema.org/). Defining the schema right before the route
helps the self-documentation of an endpoint (see usage).

This package uses jsonschema to for validation:
https://pypi.python.org/pypi/jsonschema

Usage
-----

This package provides a flask route decorator to validate json payload.

.. code:: python

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
        resp = jsonify(dict(auth_token=user.encode_auth_token(), user=user.to_dict()})
        resp.headers['Location'] = url_for('users.get_user', user_id=user.id)
        return resp, 201

The expected json payload is recognizable through "schema". If schema is
not met the requests aborts (400) with a hinting error message.

Mimetype checking
-----------------

As of 1.2.0 this decorator uses ``flask.request.get_json(force=False)``
to get the data. This means the mimetype of the request has to be
'application/json'. Can be disabled by setting ``force=False``. Be aware
that this creates a major security vulnerability to CSRF since CORS is
not enforced for certain mimetypes. Thanks to Argishti Rostamian for
noticing.

.. code:: python

    @app.route('/strict')
    @expects_json()
    def strict():
        return 'This view will return 400 if mimetype is not \'application/json\' 
        
    @app.route('/insecure')
    @expects_json({}, force=False)
    def insecure():
        return 'This view will validate the data no matter the mimetype.'

Default values
--------------

Normally validators wont touch the data. By default this package will
not fill in missing default values provided in the schema. If you want
to you can set ``fill_default=True`` explicitly. The validation will be
performed after this action, so default values can lead to invalid data.

Testing
-------

.. code:: python

    python setup.py test

Changelog
=========

`Unreleased <https://github.com/fischerfredl/flask-expects-json/compare/1.3.0...HEAD>`__
----------------------------------------------------------------------------------------

`1.3.0 <https://github.com/fischerfredl/flask-expects-json/compare/1.2.0...1.3.0>`__ - 2018-02-16
-------------------------------------------------------------------------------------------------

Changed
~~~~~~~

-  Defaults wont be filled in request data by default. Set
   fill\_defaults=True explicitly.

`1.2.0 <https://github.com/fischerfredl/flask-expects-json/compare/1.1.0...1.2.0>`__ - 2018-02-15
-------------------------------------------------------------------------------------------------

Changed
~~~~~~~

-  Security: set force=False as default argument. Before: force=True

`1.1.0 <https://github.com/fischerfredl/flask-expects-json/compare/1.0.6...1.1.0>`__ - 2018-02-03
-------------------------------------------------------------------------------------------------

Added
~~~~~

-  missing default values will be filled into the request data
-  can be turned off via fill\_defaults=False

`1.0.6 <https://github.com/fischerfredl/flask-expects-json/compare/1.0.0...1.0.6>`__ - 2018-01-29
-------------------------------------------------------------------------------------------------

-  Code-style/readme changes.
-  Add tests for Python 3.4, 3.5, 3.6
-  Changes made for proper CI and automatic release
-  Add code coverage

1.0.0 - 2018-01-21
------------------

Added
~~~~~

-  Initial version of expects\_json() decorator
-  Simple validation of request data
-  Store data in g.data

.. |version| image:: https://img.shields.io/pypi/v/flask-expects-json.svg
   :target: https://pypi.python.org/pypi/flask-expects-json
.. |license| image:: https://img.shields.io/pypi/l/flask-expects-json.svg
   :target: https://pypi.python.org/pypi/flask-expects-json
.. |pyversions| image:: https://img.shields.io/pypi/pyversions/flask-expects-json.svg
   :target: https://pypi.python.org/pypi/flask-expects-json
.. |pipeline status| image:: https://travis-ci.org/Fischerfredl/flask-expects-json.svg?branch=master
   :target: https://travis-ci.org/Fischerfredl/flask-expects-json
.. |coverage| image:: https://img.shields.io/codecov/c/github/fischerfredl/flask-expects-json.svg
   :target: https://codecov.io/gh/Fischerfredl/flask-expects-json
