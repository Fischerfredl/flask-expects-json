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
                "ipAddr": {"format": "ipv4"},
            }
        },check_formats=True )
        def dummy_route():
            return 'dummy'

        @self.app.route('/defaults')
        @expects_json({
            "type": "object",
            "properties": {
                "ipAddr": {"format": "ipv4"},
            }
        })
        def dummy_route_2():
            return 'dummy'

        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def test_format_validation_happy_path(self):
        response = self.client.get('/',
                data='{"ipAddr": "127.0.0.1"}',
                content_type='application/json')
        self.assertEqual(200, response.status_code)

    def test_format_validation_rejection(self):
        response = self.client.get('/',
                data='{"ipAddr": "-12"}',
                content_type='application/json')
        self.assertEqual(400, response.status_code)
        self.assertIn('&#x27;-12&#x27; is not a &#x27;ipv4&#x27;', response.data.decode())

    def test_format_validation_off_by_default(self):
        response = self.client.get('/defaults',
                data='{"ipAddr": "anything"}',
                content_type='application/json')
        self.assertEqual(200, response.status_code)

