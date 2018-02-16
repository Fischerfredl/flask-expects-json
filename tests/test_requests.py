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

    def test_valid_decorator(self):
        response = self.client.get('/')
        self.assertEqual(400, response.status_code)
        self.assertIn('Failed to decode', response.data.decode())
        response = self.client.get('/', data='{}', content_type='application/json')
        self.assertEqual(200, response.status_code)

    def test_check_mimetype(self):
        response = self.client.get('/schema',
                                   data='{"name": "Eggs", "price": 34.99}')
        self.assertEqual(400, response.status_code)
        self.assertIn('Failed to decode', response.data.decode())
        response = self.client.get('/schema',
                                   data='{"name": "Eggs", "price": 34.99}',
                                   content_type='application/json')
        self.assertEqual(200, response.status_code)

    def test_check_null(self):
        response = self.client.get('/schema',
                                   data='null',
                                   content_type='application/json')
        self.assertEqual(400, response.status_code)
        self.assertIn('Failed to decode', response.data.decode())
