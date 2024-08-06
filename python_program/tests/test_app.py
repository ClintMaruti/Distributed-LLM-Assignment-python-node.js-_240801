import unittest
import json
from flask import session
from app import app  # Ensure this imports the Flask app correctly

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Health 100%')

    def test_get_session_no_session(self):
        with self.app as client:
            response = client.get('/get_session')
            self.assertEqual(response.status_code, 200)
            self.assertIn('No session data found', response.data.decode('utf-8'))

    def test_select_model_llama2(self):
        with self.app as client:
            response = client.post('/select_model', json={'model': 'Llama2'})
            data = json.loads(response.data.decode('utf-8'))
            self.assertEqual(response.status_code, 200)
            self.assertIn('Llama2 model initialized', data['message'])
            self.assertIsNotNone(data['session_id'])
            with client.session_transaction() as sess:
                self.assertEqual(sess['model'], 'Llama2')

    def test_select_model_mistral(self):
        with self.app as client:
            response = client.post('/select_model', json={'model': 'Mistral'})
            data = json.loads(response.data.decode('utf-8'))
            self.assertEqual(response.status_code, 200)
            self.assertIn('Mistral model initialized', data['message'])
            self.assertIsNotNone(data['session_id'])
            with client.session_transaction() as sess:
                self.assertEqual(sess['model'], 'Mistral')

    def test_select_model_invalid(self):
        response = self.app.post('/select_model', json={'model': 'InvalidModel'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data['error'], 'Invalid model selected')

    def test_chat_no_model(self):
        response = self.app.post('/chat', json={'query': 'Hello'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data['error'], 'No model selected')

    def test_chat_no_query(self):
        with self.app as client:
            client.post('/select_model', json={'model': 'Llama2'})
            response = client.post('/chat', json={})
            self.assertEqual(response.status_code, 400)
            data = json.loads(response.data.decode('utf-8'))
            self.assertEqual(data['error'], 'Query not provided')

    def test_chat_llama2(self):
        with self.app as client:
            client.post('/select_model', json={'model': 'Llama2'})
            with client.session_transaction() as sess:
                sess['session_id'] = 'test-session-id'
            response = client.post('/chat', json={'query': 'Hello'})
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data.decode('utf-8'))
            self.assertIn('response', data)

    def test_chat_mistral(self):
        with self.app as client:
            client.post('/select_model', json={'model': 'Mistral'})
            with client.session_transaction() as sess:
                sess['session_id'] = 'test-session-id'
            response = client.post('/chat', json={'query': 'Hello'})
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data.decode('utf-8'))
            self.assertIn('response', data)

if __name__ == '__main__':
    unittest.main()
