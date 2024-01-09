from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
from text_cleaner import clean_text
import boto3
import pickle
import psycopg2
from flasgger import Swagger
from flask_cors import CORS
import os

"""
Performs sentiment analysis on text data from pre-trained model.
Updates database with the results of the analysis.
"""

app = Flask(__name__)
CORS(app)

is_docker_environment = os.getenv('DOCKER') == 'true'

if (is_docker_environment):
    swagger = Swagger(app, template_file='sentiment_swagger.yaml')
else:
    swagger = Swagger(app, template_file='docs/sentiment_swagger.yaml')

# Set your AWS credentials and region
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = 'us-east-1'
bucket_name = 'mhapy-sentiment-analysis'
model_key = 'big_data_seq_150.h5'

# Set the path where you want to save the downloaded model
if (is_docker_environment):
    local_model_path = 'aws_lstm.h5'
else:
    local_model_path = 'trained_models/aws_lstm.h5'

with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# Download model .h5 from s3 bucket
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)
s3.download_file(bucket_name, model_key, local_model_path)

# Load the trained model
clf = load_model(local_model_path, compile=True)

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

print("Backend is ready")

@app.route('/update-database', methods=['POST'])
def update_database():
    try:
        # Get user_id from the POST request
        user_id = request.json.get('user_id')
        text_data = request.json.get('text')
        time = request.json.get('time')
        sentiment_data = request.json.get('sentiment')
        score_data = request.json.get('score')
        # Check if any data is missing from POST request
        if any(data is None for data in [user_id, text_data, time, sentiment_data, score_data]):
            return jsonify({'error': 'Missing data in the request'}), 400

        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Perform SQL query with parameterized query to avoid SQL injection
        insert_query = """
        INSERT INTO text_sentiment (text, user_id, time, sentiment, score)
        values (%s, %s, TIMESTAMP %s, %s, %s);
        """
        cursor.execute(insert_query, (text_data, user_id, time, sentiment_data, score_data))

        connection.commit()
        # Close the cursor and connection
        cursor.close()
        connection.close()

        return jsonify({'status': 'success'}), 200
    except Exception as e:
        print(f"Error in update_database: {str(e)}")

        # If an error occurred, return an error status code
        return jsonify({'status': 'error'}), 500


@app.route("/compute-sentiment", methods=["POST"])
def predict():
    try:
        # Get input data from the request
        data = request.json.get('text')
        if not data:
            return jsonify({'error': 'Text data is missing in the request'}), 400

        # Perform sentiment analysis using your model
        cleaned_text = clean_text(data)

        # Tokenize and pad the input sequence
        tokenized_message = tokenizer.texts_to_sequences([cleaned_text])
        tokenized_message = pad_sequences(tokenized_message, maxlen=150)

        # Make the prediction
        prediction = clf.predict(tokenized_message)
        predicted_label = np.argmax(prediction)
        # Create a response dictionary
        response_data = {
            'prediction': int(predicted_label),
            'probability': float(prediction[0][predicted_label] * 100)
        }
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test', methods=['GET'])
def test_endpoint():
    try:
        # Attempt to return the JSON response
        response_data = {'message': 'This is a test endpoint on the sentiment Flask API'}
        return jsonify(response_data), 200
    except Exception as e:
        # If an error occurs while returning the JSON response, return a 500 error
        return jsonify({'error': 'Failed to process the request'}), 500


if __name__ == '__main__':
    # Run the Flask application on all network interfaces, port 5005
    app.run(host='0.0.0.0', port=5005)
