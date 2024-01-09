import psycopg2
import os

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Retrieves data from mhapy's PostgreSQL sentiment database hosted on AWS RDS.
# Returns json file containing db data concerning the app user, specified by user_id.
def get_data(user_id):

    # Connect to the PostgreSQL database
    connection = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    # PostgreSQL query
    query = "SELECT time, sentiment, score FROM text_sentiment WHERE user_id = %s;"
    # Create cursor, use it to execute query on db with given user_id
    cursor = connection.cursor()
    cursor.execute(query, (user_id,))
    results = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    return results

