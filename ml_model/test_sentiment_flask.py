import unittest
import json
from unittest.mock import patch
from sentiment_flask import app
class TestSentimentFlask(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_compute_sentiment(self):
        data = {'text': 'This is a test message for sentiment analysis'}
        response = self.app.post('/compute-sentiment', json=data)
        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.data)
        self.assertIn('prediction', response_data)
        self.assertIn('probability', response_data)

    def test_update_database(self):
        data = {
            'user_id': "Test User 1",
            'text': 'I am so happy today',
            'time': '2023-11-16 12:00:00',
            'sentiment': 1,
            'score': 80.43
        }
        response = self.app.post('/update-database', json=data)
        self.assertEqual(response.status_code, 200)

    def test_test_endpoint(self):
        response = self.app.get('/test')
        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.data)
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], 'This is a test endpoint on the sentiment Flask API')

    @patch('sentiment_flask.psycopg2.connect')
    def test_update_database_missing_data(self, mock_connect):
        mock_connection = mock_connect.return_value
        mock_cursor = mock_connection.cursor.return_value

        data = {
            'user_id': "Test User 1",
            'time': '2023-11-16 12:00:00',
            'sentiment': 0,
            'score': 75.4
        }
        response = self.app.post('/update-database', json=data)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()