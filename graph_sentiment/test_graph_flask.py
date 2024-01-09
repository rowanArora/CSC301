import unittest
import json
from graph_flask import app 

class TestFlaskAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_graph_endpoint(self):
        payload = {'user_id': "Test User 1"}  # Replace with appropriate user_id for testing

        response = self.app.post('/get-graph', json=payload)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertIn('graph_html', data)
        # Add more assertions based on expected response for successful graph generation

    def test_missing_user_id_get_graph_endpoint(self):
        payload = {}  # No user_id provided

        response = self.app.post('/get-graph', json=payload)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        # Add more assertions based on expected response for missing user_id

    def test_failed_to_get_data_get_graph_endpoint(self):
        payload = {'user_id': "JASDJKJASKDJCNXZZXC<MNW"}  # Assuming this user_id doesn't exist in your test data

        response = self.app.post('/get-graph', json=payload)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 404)
        self.assertIn('error', data)

    def test_test_endpoint(self):
        response = self.app.get('/test')

        self.assertEqual(response.status_code, 200)
        self.assertIn('message', json.loads(response.data.decode()))
        
if __name__ == '__main__':
    unittest.main()
