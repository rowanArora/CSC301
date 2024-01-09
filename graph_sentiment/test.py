import unittest
from api_graph import create_graph

class TestCreateGraph(unittest.TestCase):

    def test_create_graph_with_valid_data(self):
        # Test the function with valid data and check if it returns a non-empty result
        db_data = [
            ('2023-01-01', 1, 50),
            ('2023-01-02', 1, 100),
            ('2023-01-03', 0, 0)
        ]
        result = create_graph(db_data)
        self.assertTrue(result)  # Check if the result is non-empty

    def test_create_graph_with_empty_data(self):
        # Test the function with empty data and check if properly handles the error
        db_data = []
        with self.assertRaises(ValueError) as context:
            create_graph(db_data)
        self.assertEqual(str(context.exception), "No data to graph.")  

    def test_create_graph_with_missing_sentiment(self):
        # Test the function with missing sentiment data and check if it handles it properly
        db_data = [
            ('2023-01-01', None, 66),
            ('2023-01-02', None, 88),
            ('2023-01-03', None, 33)
        ]
        with self.assertRaises(ValueError) as context:
            create_graph(db_data)
        self.assertEqual(str(context.exception), "Improper sentiment values. Expecting 0 or 1.")  

    def test_create_graph_with_invalid_sentiment(self):
        # Test the function with invalid sentiment data and check if it handles it properly
        db_data = [
            ('2023-01-01', 2, 5),
            ('2023-01-02', -2, 8),
            ('2023-01-03', 0, 3)
        ]
        with self.assertRaises(ValueError) as context:
            create_graph(db_data)
        self.assertEqual(str(context.exception), "Improper sentiment values. Expecting 0 or 1.") 

    def test_create_graph_with_missing_score(self):
        # Test the function with missing score data and check if it handles it properly
        db_data = [
            ('2023-01-01', 1, None),
            ('2023-01-02', 1, None),
            ('2023-01-03', 0, None)
        ]
        with self.assertRaises(ValueError) as context:
            create_graph(db_data)
        self.assertEqual(str(context.exception), "Sentiment scores out of range. Expecting values between 0 and 100 inclusive.")  

    def test_create_graph_with_invalid_score(self):
        # Test the function with invalid score data and check if it handles it properly
        db_data = [
            ('2023-01-01', 1, -1),
            ('2023-01-02', 0, 101),
            ('2023-01-03', 1, 0)
        ]
        with self.assertRaises(ValueError) as context:
            create_graph(db_data)
        self.assertEqual(str(context.exception), "Sentiment scores out of range. Expecting values between 0 and 100 inclusive.")  
    

if __name__ == '__main__':
    unittest.main()
