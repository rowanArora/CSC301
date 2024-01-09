# Import packages
from flask import Flask, request, jsonify
from get_data import get_data
from api_graph import create_graph
from flasgger import Swagger
from flask_cors import CORS
import os
"""
Generates a graph that plots sentiment analysis data over time.
Deploys the graph to a server via dash.
"""

app = Flask(__name__)
CORS(app)

is_docker_environment = os.getenv('DOCKER') == 'true'

if (is_docker_environment):
    swagger = Swagger(app, template_file='graph_swagger.yaml')
else:
    swagger = Swagger(app, template_file='docs/graph_swagger.yaml')

@app.route('/get-graph', methods=['POST'])
def get_graph():
    try:
        # Get user_id from the POST request
        user_id = request.json.get('user_id')

        if not user_id:
            # If user_id is missing in the request, return 400 Bad Request
            return jsonify({'error': 'User ID is missing in the request'}), 400

        # Retrieve data from db concerning user_id
        results = get_data(user_id)

        if not results:
            # If no data found for the specified user_id, return 404 Not Found
            return jsonify({'error': 'User ID is not found in database'}), 404
        
        # Process the results and create a graph
        graph = create_graph(results)  # graph is html div

        if not graph:
            return jsonify({'error': 'Failed to create the graph'}), 500
        return jsonify({'graph_html': graph}), 200

    except Exception as e:
        return jsonify({'error': 'Graph Flask Internal Server Error'}), 500
    
@app.route('/test', methods=['GET'])
def test_endpoint():
    try:
        # Attempt to return the JSON response
        response_data = {'message': 'This is a test on graph Flask API endpoint'}
        return jsonify(response_data), 200
    except Exception as e:
        # If an error occurs while returning the JSON response, return a 500 error
        return jsonify({'error': 'Failed to process the request'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
