import unittest
import flask

from flask_expects_json import expects_json


class TestExpects(unittest.TestCase):
    def setUp(self):
        self.app = flask.Flask(__name__)

        @self.app.route('/', methods=['GET', 'HEAD', 'POST'])
        @expects_json()
        def all_requests():
            return 'happy'

        @self.app.route('/ignore_one', methods=['GET', 'HEAD', 'POST'])
        @expects_json(ignore_for=['GET'])
        def ignore_get():
            return 'happy'

        @self.app.route('/ignore_two', methods=['GET', 'HEAD', 'POST'])
        @expects_json(ignore_for=['GET', 'HEAD'])
        def ignore_get_head():
            return 'happy'

        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def test_default_behaviour(self):
        response = self.client.get('/')
        self.assertEqual(400, response.status_code)
        self.assertIn('Failed to decode', response.data.decode())
        response = self.client.head('/')
        self.assertEqual(400, response.status_code)
        response = self.client.get('/', data='{}', content_type='application/json')
        self.assertEqual(200, response.status_code)

    def test_ignore_one(self):
        response = self.client.get('/ignore_one')
        self.assertEqual(200, response.status_code)
        response = self.client.head('/ignore_one')
        self.assertEqual(400, response.status_code)
        response = self.client.post('/ignore_one', data='')
        self.assertEqual(400, response.status_code)
        self.assertIn('Failed to decode', response.data.decode())
        response = self.client.get('/ignore_one', data='{}', content_type='application/json')
        self.assertEqual(200, response.status_code)

    def test_ignore_multiple(self):
        response = self.client.get('/ignore_two')
        self.assertEqual(200, response.status_code)
        response = self.client.head('/ignore_two')
        self.assertEqual(200, response.status_code)
        response = self.client.post('/ignore_two', data='')
        self.assertEqual(400, response.status_code)
        self.assertIn('Failed to decode', response.data.decode())
        response = self.client.get('/ignore_two', data='{}', content_type='application/json')
        self.assertEqual(200, response.status_code)
