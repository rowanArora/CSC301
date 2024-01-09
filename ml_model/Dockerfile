# Use a base image with Python pre-installed
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Define build arguments for AWS credentials
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG DB_HOST
ARG DB_PORT
ARG DB_NAME
ARG DB_USER
ARG DB_PASSWORD

# Set environment variables with the build arguments
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
ENV DB_HOST=$DB_HOST
ENV DB_PORT=$DB_PORT
ENV DB_NAME=$DB_NAME
ENV DB_USER=$DB_USER
ENV DB_PASSWORD=$DB_PASSWORD

ENV DOCKER=true

# Copy the Python script and requirements file to the container
COPY sentiment_flask.py flask_requirements.txt text_cleaner.py tokenizer.pickle docs/sentiment_swagger.yaml /app/

# Install required dependencies and set up the virtual environment
RUN python -m venv venv
RUN /bin/bash -c "source venv/bin/activate && pip install --no-cache-dir -r flask_requirements.txt"

# Expose the container's port
EXPOSE 5005

# Command to start the sentiment Flask application
CMD ["/bin/bash", "-c", "source venv/bin/activate && gunicorn -w 1 -b 0.0.0.0:5005 sentiment_flask:app"]

