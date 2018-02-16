import unittest
import flask

from flask_expects_json import expects_json


class TestDefaults(unittest.TestCase):
    def setUp(self):
        self.app = flask.Flask(__name__)

        @self.app.route('/')
        @expects_json({
            "type": "object",
            "properties": {
                "price": {"type": "number", "default": 5.3},
                "name": {"type": "string", "default": "hubert"},
                "tags": {"type": "array"}
            }
        }, fill_defaults=True)
        def happy():
            return 'happy'

        @self.app.route('/invalid')
        @expects_json({
            "type": "object",
            "properties": {
                "name": {"type": "string", "default": 5}
            }
        }, fill_defaults=True)
        def invalid_default():
            return ''

        @self.app.route('/valid')
        @expects_json({
            "type": "object",
            "properties": {
                "name": {"type": "string", "default": 5}
            }
        })
        def default():
            return ''

        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def test_default_works(self):
        response = self.client.get('/',
                                   data='{}',
                                   content_type='application/json')
        self.assertEqual(200, response.status_code)
        self.assertIn('price', flask.g.data)
        self.assertIn('name', flask.g.data)
        self.assertEqual(5.3, flask.g.data['price'])
        self.assertIn('hubert', flask.g.data['name'])

    def test_default_gets_validated(self):
        response = self.client.get('/invalid',
                                   data='{}',
                                   content_type='application/json')
        self.assertEqual(400, response.status_code)
        self.assertIn('5 is not of type \'string\'', response.data.decode())

    def test_default_off_by_default(self):
        response = self.client.get('/valid',
                                   data='{}',
                                   content_type='application/json')
        self.assertEqual(200, response.status_code)

    def test_setdefault_on_string(self):
        @self.app.route('/strings')
        @expects_json({
            "type": "object",
            "properties": {
                "name": {"type": "string", "default": "hubert"}
            }
        }, fill_defaults=True)
        def default_on_string():
            return 'happy'

        response = self.client.get('/strings',
                                   data='"invalid"',
                                   content_type='application/json')
        self.assertEqual(400, response.status_code)
