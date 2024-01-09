# Use a base image with Python pre-installed
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

ARG DB_HOST
ARG DB_PORT
ARG DB_NAME
ARG DB_USER
ARG DB_PASSWORD

ENV DB_HOST=$DB_HOST
ENV DB_PORT=$DB_PORT
ENV DB_NAME=$DB_NAME
ENV DB_USER=$DB_USER
ENV DB_PASSWORD=$DB_PASSWORD

ENV DOCKER=true

# Copy the Python script and requirements file to the container
COPY graph_flask.py flask_requirements.txt get_data.py read_data.py api_graph.py docs/graph_swagger.yaml /app/

# Create and activate a virtual environment
RUN python -m venv venv
SHELL ["/bin/bash", "-c"]  # Change shell to Bash to run source command
RUN /bin/bash -c "source venv/bin/activate && pip install --no-cache-dir -r flask_requirements.txt"

# Expose the container's port
EXPOSE 5001

# Command to start the graph Flask application 
CMD ["/bin/bash", "-c", "source venv/bin/activate && gunicorn -w 1 -b 0.0.0.0:5001 graph_flask:app"]

