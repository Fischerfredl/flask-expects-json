# flask-json-expects

Decorator for REST endpoints in flask. Validate JSON request data.

When building json REST services I find myself already specifying json-schema for POST data while defining swagger spec. This package brings json validation to flask. It omits the need to validate the data yourself while profiting from an already established standard (http://json-schema.org/). Defining the schema right before the route helps the self-documentation of an endpoint (see usage).


This package uses jsonschema to for validation: https://pypi.python.org/pypi/jsonschema



## Usage

This package provides a flask route decorator to validate json payload.

```python 
from flask import Flask
from flask_expects_json import expects_json

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

    user = User().from_dict(g.data)
        try:
        user.save()
    except (ValidationError, NotUniqueError) as e:
        return abort(400, e.message)

    resp = jsonify({'auth_token': user.encode_auth_token(), 'user': user.to_dict()})
    resp.headers['Location'] = url_for('users.get_user', user_id=user.id)
    return resp, 201
```

The expected json payload is recognizable through schema. If schema is not met the requests aborts (400) with a hinting error message.

```flask.request.get_json(force=True)``` is used to get the data. This means the mimetype of the request is ignored.

## Testing

```python
python setup.py test
```

For coverage use the python coverage package. See ```/cov.sh``` for usage. 

```./cov.sh``` will pip install coverage. So make sure to use it in the context of your virtual env.
