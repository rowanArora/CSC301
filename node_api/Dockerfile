FROM node:18-slim

# Set working directory
WORKDIR /app

# Run command to update the system
RUN apt-get update

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY

ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY

ENV DOCKER=true

# Copy package.json and package-lock.json into image/container
COPY package*.json ./

# Install appropriate packages using npm
RUN npm install

COPY . .

# Run the Node.js application
CMD ["node", "src/index.js"]
