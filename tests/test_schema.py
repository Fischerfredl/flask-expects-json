import unittest
import flask

from flask_expects_json import expects_json


class TestExpects(unittest.TestCase):
    def setUp(self):
        self.app = flask.Flask(__name__)

        @self.app.route('/')
        @expects_json()
        def no_schema():
            return 'happy'

        @self.app.route('/schema')
        @expects_json({
            "type": "object",
            "properties": {
                "price": {"type": "number"},
                "name": {"type": "string"},
            },
            "required": ["price"]
        })
        def schema():
            return 'happy'

        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def test_validation_valid(self):
        response = self.client.get('/schema',
                                   data='{"name": "Eggs", "price": 34.99}',
                                   content_type='application/json')
        self.assertEqual(200, response.status_code)
        self.assertEqual('Eggs', flask.g.data['name'])
        self.assertEqual(34.99, flask.g.data['price'])

    def test_validation_invalid(self):
        response = self.client.get('/schema',
                                   data='{"name": "Eggs", "price": "invalid"}',
                                   content_type='application/json')
        self.assertEqual(400, response.status_code)
        self.assertIn('is not of type \'number\'', response.data.decode())

    def test_missing_parameter(self):
        response = self.client.get('/schema',
                                   data='{"name": "Eggs"}',
                                   content_type='application/json')
        self.assertEqual(400, response.status_code)
        self.assertIn('is a required property', response.data.decode())

    def test_additional_parameter(self):
        response = self.client.get('/schema',
                                   data='{"name": "Eggs", "price": 34.99}',
                                   content_type='application/json')
        self.assertEqual(200, response.status_code)
