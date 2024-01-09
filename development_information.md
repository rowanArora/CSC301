# Development Information and Requirements

## Project Architecture
The project is composed of three main components: 
* Node.js Controller
* Flask Sentiment
* Flask Visualizer

The Node.js Controller file serves as the main entry point of the API which has three main endpoints: a **GET** request called `/scrape-text` to scrape and siphon journal text data, a **POST** request called `/analyze-sentiment` to analyze a sentiment's text from a user, and another **POST** request `retrieve-graph` which retrieves a graph of a user.

The Flask Sentiment file has two main endpoints: a **POST** request `/compute-sentiment` which predicts sentiment of a text using the model and another **POST** request, `/update-database`, which inserts new sentiment data into the database.

The Flask Vizualizer file has one main endpoint: a **POST** request `/get-graph` which generates a graph of a given user's sentiment data.

Each of these files also have a test endpoint to ensure that each backend file is running.

## External Components (Docker Hub & AWS)
For each of the components, they utilize a container for every route handler file as each component has a Dockerfile to build the image to run the container.
We utilized `Docker Compose` to build all containers at once. These built images will be pushed to `Docker Hub`. 

We chose to deploy these two different `Amazon EC2` instances, one as a testing/staging environment and the other is the production environment for use but they both function as the same. The testing/staging environment EC2 is called `mhapy-sentiment-test-stage` and the production environment ec2 is called `mhapy-sentiment-docker`

We also employed the use of `Amazon RDS` which hosts a PostgreSQL sentiment database which consists of `text`, `user_id`, `time` `sentiment` and `score`, as the latter two columns will be discussed down below. And as mentioned before the time needs to be in ISO 8601 format. The database identifier name on AWS is called `sentimentdb`.

The last thing we used was `Amazon S3` which hosts our raw journal text `sentiment_journal_text.json` scraped from the mhapy backend database, which we used once to train the model. And also of course the sentiment analysis machine learning model `big_data_seq_150.h5` which we will use to predict new sentiment.

One last file is located in the S3 bucket called `sentiment_api_secrets.txt` with the credentials for all of the above and more. The section at the bottom has more information.
The production and deployment are all done through GitHub Actions and will be discussed below in the DevOps section.

### API Workflow Description
Here is an SVG flowchart depicting the architecture of the API and we'll discuss this right underneath.

<p align="center">
  <img src="/resources/architecture_flowchart.svg"/>
</p>

> If it's hard to see try to open this in a new tab, and you can zoom into each element.

#### /analyze-sentiment
Starting with the Node.js server, where the main POST request exists at `/analyze-sentiment`. The endpoint accepts a POST request with a body that includes a user's: 
* Text
* User ID
* Time
* Email

Mhapy’s API should call for a POST request at this endpoint to send the user id, text, time, and email to the Node.js server. Afterwards, this same endpoint will call for another POST request which sends the given text to the `/compute-sentiment` located in the Flask Sentiment application.

The flask application on startup will download and load in the sentiment analysis model into the file which allows the program to be available to predict sentiment at any time. The flask program first cleans the text and will then predict the sentiment which is a value of either a *0 or 1*.

A 0 indicates a positive text and a 1 being a negative text. It also provides a sentiment score which is a scale from 0 to 100 being based on how positive or negative the text is. These values will be returned as a json back to the Node.js server. 

Immediately afterwards, the same `/analyze-sentiment` will test if the sentiment was a 1 (negative) and if the score was greater than **95**, which we declared as an extreme negative sentiment. The API will automatically send an ***email*** to the user giving them a message of support and mental health services. 

It will then always call for another POST request at another endpoint `/update-database` on the same sentiment flask program.

This request body will take in five properties:
* Text
* User ID
* Time
* Sentiment
* Score
  
The last two fields (sentiment & score) are from the `/compute-sentiment` endpoint that which `/analyze-sentiment` called. 

The controller Node.js `/analyze-sentiment` endpoint will then call one last POST request with a request body of just the user id to the endpoint `/get-graph` on the graph flask application. 

This `/get-graph` endpoint calls two distinct helper functions in order to return a Plotly graph. First, we call the get_data function from `get_data.py` which retrieves all of the sentiment data belonging to the user of the given user id. This is done using psycopg2 which allows our python program to fetch data from our relational database. Next we call our create_graph function from api_graph.py. 

This function takes the data retrieved from get_data and translates it into a Plotly graph. Within this helper function, we have to modify the retrieved data by separating it into positive and negative data, allowing us to clearly show both the positive and negative sentiment side by side. Lastly, we return our Plotly graph as a jsonified html div element.

The Node.js server will return this HTML graph to the original mhapy backend API for them to use, allowing the user to easily view the graph on their own device.

#### /scrape-text

The next endpoint is a GET request `/scrape-text` separated from the main `/analyze-sentiment` endpoint on the Node.js server which scrapes the data directly from an endpoint off of mhapy’s backend API, where it feeds us the data from the mhapy journal text database. 

This data consists of every user's journal entry which includes the text they inputted, their user id, the time the user made the entry, their email and much more information given. Our endpoint is exposed at as a  which is in charge of downloading the data as a json for us to train our model on. 

It siphons out useless data except for information we need like their user_id, text, time and email. The data scraped by the Node.js API will also be uploaded to the same database with its sentiment scores trained on it. This old journal text will be stored along with new text sentiment, allowing previous history to be displayed with the new data on the graph.

The graph generated from `/analyze-sentiment` and `/retrieve-graph` will also make use of this scraped data from the mhapy database of journal text which is inserted into the sentiment database.

#### /retrieve-graph
The last endpoint that should be called is the POST request `/retrieve-graph` endpoint accepting a request body of:
* User ID

This will call a POST request to the `/get-graph` on the Flask Visualizer with the same request body and afterwards will return a graph in json format. Similar to the `/analyze-sentiment` endpoint, it will return this back up to the Node.js application. The main difference in this endpoint and the others is that this does not insert a new data point in the database but rather only retrieves data. This json can also be rendered by redirecting the output to an HTML.

## Repository Organization
Our code is all sorted into the directory which consists of three main subdirectories, one for each component of the project.
The first is the `node_api` directory which hosts the Node.js Controller route handler file serving as the main entry point access the API. The second subdirectory is the `ml_model` folder which hosts files which helped the train the model along with the integrated backend file responsible for performing the sentiment analysis. Then the last subdirectory `graph_sentiment` hosts the graph generating service which creates a visualization of the sentiments values from the user. 

Another subdirectory exists which is the `.github/workflows` directory which hosts all of the GitHub Actions Workflows .yml files used to produce and deploy the app. These files are for the DevOps portion of the application.

One last additional file exists to help production and deployment which is the `docker-compose.yml` which will be used to build, push, run and stop containers of each of these files.

Finally, one extra subdirectory exists, `resources`, which includes images for the README.md. 

Edit the .gitignore, LICENSE, README however you would like.
The deliverables subdirectory is irrelevant to the code and is for CSC301.

### Node.js Controller Structure
In the `node_api` directory, we built the Node.js application using npm so there is a package.json and package-lock.json files there to hold our dependencies. The src directory holds both the `index.js` and `swagger.js` files. The `index.js` file is where all of our code exists for the API, responsible for the /scrape-text, /analyze-sentiment, and /retrieve-graph. The `docs` subdirectory hosts the Swagger Documentation called `node_swagger.yaml` which the `swagger.js` file connects to. 

In the `public` directory, we have an `index.html` to help simulate a POST request to our API and a stylesheet `styles.css` to create a presentable basic frontend. 

Another file named `swagger.js` in the src folder is responsible for importing the `node_swagger.yaml` documentation located in the `docs` subdirectory. 

There is also a subdirectory called `test` which hosts one file named `index.test.js` which is used as the test file.

The `config` directory has a file called `low_sentiment_email.yaml` which is the template email we created for sending emails to patients with extremely dangerous low sentiment. Feel free to change any of the subject, body and who it is from. We have provided credentials for the login details for the email "mhapy.noreply@gmail.com" in the tokens/credentials txt file on the AWS S3, more information for that file is available below. 

There also exists a Dockerfile responsible for building this Node.js application in a Docker container.

### Flask Sentiment Structure
Many files in this directory were for training the model with for us to train the model on, `model.py` and `model_test.py` and the `tokenizer.pickle` a the tokenizer which is essential to use the model with.
Then we have the `sentiment_flask.py` which is the actual flask application that will be ran to call requests to. The `flask_requirements.txt` are the dependencies that should be installed with `pip`. The `text_cleaner.py` program is used inside the flask app which was used to preprocess the text given to it to predict an output.

The `data` directory holds csv files of the data we trained our ML model on which we compiled into a singular data set. The next subdirectory is `trained_models` which hosts our trained sentiment ML models inside of it the main one being `aws_lstm.h5` which we renamed the other file `big_data_seq_150.h5` hosted on the AWS S3 bucket once we download it. The last relevant subdirectory is `docs` which holds one file `sentiment_swagger.yaml` which is the Swagger Documentation for the Flask Sentiment file for the endpoints.

Similar to the Node.js application, a Dockerfile responsible for building this Flask application in a Docker container.

### Flask Visualizer Structure
This flask application is more modularized than the rest composing of separate files to generate the visualization. The `graph_flask.py` is the actual flask application which will be ran to call requests to. The sub components that make up `graph_flask.py` are `get_data.py` which is used to retrieve data from the database and the `api_graph.py` is responsible for creating the graph of these sentiments. Again, the `flask_requirements.txt` are the dependencies that should be installed with `pip`. There are two additional files one for the flask application and the other for the general graph visualizer called `test_graph_flask.py` and `test.py` respectively. 

The `docs` subdirectory also holds one file `graph_swagger.yaml` which is the Swagger Documentation for the Flask Sentiment file for the endpoints. And of course there also exists a Dockerfile responsible for building this flask application in a Docker container.

## Essential Modules & Components

### Node.js Controller Details
* `Express`
  * Express was used as the web application framework simplifying routing for efficient server-side development.
* `Axios`
  * We used this call HTTP requests to each endpoint.
* `Nodemailer`
  * The Node.js application used to send the emails to the user through this package.

### Flask Sentiment Details
* `TensorFlow`
  * Used to train our machine learning model with a more mature ecosystem with extensive support.
* `NLTK`
  * Used a lemmatizer normalizes words to their base form. Simplifies word analysis and language processing in NLTK.
  * NLTK stopwords are common words filtered out to enhance natural language processing by eliminating noise.
* `psycopg2`
  * A Python adapter for PostgreSQL used to call INSERT SQL statements.
  * Used an INSERT SQL query through /update-database to insert text, user_id, time, sentiment and score on the Amazon RDS sentiment database.
* `boto3`
  * An SDK used to download the ML model (.h5 file) off of the S3 bucket.
  
### Flask Visualizer Details
* `Plotly`
  * Plotly is a versatile data visualization library and helps create interactive and appealing visualizations easily.
* `psycopg2`
  * A Python adapter for PostgreSQL used to call SELECT SQL statements.
  * Used an SELECT SQL query on /get-graph through the get_data.py file to select time, sentiment and score from the given user in the Amazon RDS sentiment database.

### Documentation
To document our API, we used three separate `Swagger` .yaml files to provide information for each endpoint created. Each backend program file’s endpoints will send back appropriate HTTP response codes, depending on scenarios such as if they don’t fulfill the POST request requirements, an internal server error occurred or if it was a successful response along with many other scenarios. Alongside this, we have also included comments which explain what the API is doing to guide the engineer through the code.

## Sentiment Analysis Model Architecture
The actual sentiment analysis functionality for our project was implemented through a Bidirectional LSTM model. This model was trained on several different Kaggle datasets as well as a smaller dataset provided to us by our partner. Our model architecture starts with an Embedding layer with masking on the padded label-encoded string followed by a sequence of Bidirectional LSTM layers with recurrent dropout, and with Dropout and Dense layers containing the ReLU activation function sprinkled in between. There is a final Dense layer with the Softmax activation function at the end for the output layer. We added early stopping to the model in the hopes of preventing any possible overfitting and shortening the training time of the model. We decided to use the Adam Optimizer to hopefully improve the optimization of our model. The goal of this was to enhance the training efficiency and convergence speed. The Adam Optimizer combines the benefits of two extensions of Stochastic Gradient Descent: the Adaptive Gradient Algorithm (AdaGrad) and Root Mean Square Propagation (RMSProp). The Adam Optimizer adjusts the learning rates for each parameter individually, allowing for more efficient training across different dimensions and scales.

## Deployment and Github Workflow
First of all we created a D3 directory and posted all of our code into three folders for each of our subteams because we had split the work into three branches corresponding to the three API's. So to continue working on this, we created branches inside of this main repository to split the work again to continue working on each API separately and once we had an update we merged them back to main through pull requests of those separate API branches. We had one member from another subteam of a different API review the pull request and if successful merge the separate API branch into the main branch. We tried to keep each branch responsible for one issue to keep the pull requests simple. We then moved these out of the D3 directory once we were finished.

We also made a deployment branch that attempted to incorporate all three of these API's together and deploy it on an EC2 instance. For some naming conventions, we use pothole case in the Python API's and camel case in the Node.js API. We found this workflow to be the best since it allowed us to work on each of the parts separately while being able to help each other by going to their branch to help fix their code and this was the most flexible option allowed the most freedom. When certain merge conflicts appear, we come together as a group and try to solve each one determining which commit should be added to the main branch.

### Deployment and Automation (DevOps)
We decided to use Docker to simplify the deployment and GitHub Actions to implement CI/CD to the project to streamline the process of integration and deployment. These additions overall clean up the deployment process as it removed a bunch commands, install dependencies, start and restart the deployment whether it be local or on a server.

#### Docker Compose
We used a `docker-compose.yml` file which builds each component in its own container labeled `mhapy-node-container`, `mhapy-ml-container`, and `mhapy-graph-container`. Each will be built as an image and pushed to the Docker Hub repository with a tag labeled `<DOCKERHUB_USERNAME>/mhapy_node_img:latest`, `<DOCKERHUB_USERNAME>/mhapy_ml_img:latest`, `<DOCKERHUB_USERNAME>/mhapy_graph_img:latest` respectively. The real Docker Hub username is listed in the secret tokens txt file. Then it is ran on a Docker Network called `mhapy-sentiment-network` which connects all three containers allowing them to call requests to one another.

We containerized the deployment without Amazon ECR and ECS but through DockerHub using an Ubuntu EC2 instance. Then we made sure any traffic from any IP could visit and access the API through the AWS Management Console.  

### CI/CD Workflows
Here is a flowchart diagram of our deployment process:

<p align="center">
  <img src="/resources/deployment_flowchart.svg"/>
</p>
> Feel free to open this up and zoom in to each element.

For this project, our CI/CD workflow was composed of three main parts:
* **Testing** phase
* **Image production** phase
* **Deployment** phase

The first would be the `test-node-flask.yml` file which runs test cases on all three route handler files which are the Node.js Controller, Flask Sentiment, Flask Graph and ensures they work. Each of these test case files are located in each of the subdirectories: `node_api` which has the test/index.test.js, `ml_model` which has the test_sentiment_flask.py and `graph_sentiment` which has the test_graph_flask.py file. 

Afterwards, the `docker-create.yml` is activated on test-node-flask.yml's successful completion which will build the Docker images and push them to Docker Hub using Docker Compose. 

Then finally the deployment phase is initiated after docker-create.yml successfully completes which in turn activates both `deploy-testing-ec2.yml` and `deploy-production-ec2.yml`. The first workflow file ssh's into a testing/staging environment on an Amazon EC2 instance which pulls the images from Docker Hub, creates a Docker Network and runs all three containers on that network. 

Alongside the first workflow, the other file `deploy-production-ec2.yml` is responsible for doing a similar task but this time it deploys to a production environment EC2 instance instead thus completing the CI/CD workflow until another commit to the repository is made.

### Accessing AWS Services or Docker Hub
If for whatever reason, you'd like to edit or access any of the external services here are instructions for you.

#### AWS EC2
1. Login to AWS with your account.
2. Navigate to the EC2 instances on us-east-1 server
3. Choose the `mhapy-sentiment-docker` for the production environment or the `mhapy-sentiment-test-stage` for the testing/staging environment
4. Click **Connect** on the top.
5. Connect however you would like, whether EC2 instance connect or through the console
6. If using console, follow these instructions to SSH into the instance

<p align="center">
  <img src="/resources/ssh_in.png"/>
</p>

> Note: The mhapy-sentiment.pem key is located in the S3 bucket as well, please download that.

7. Now you should be into the Ubuntu console free to do whatever.

If you'd like to change the security groups (who can access this API)
1. Go back to AWS EC2 instances page and highlight the chosen instance
2. Click on the Security tab underneath the EC2 instance
3. Click on the Security Group, i.e.:

<p align="center">
  <img src="/resources/security_group.png"/>
</p>

4. Click on **Edit inbound rules**
5. Then change the each of the type to suit your needs along with the specific IP's allowed to access these

<p align="center">
  <img src="/resources/change_inbound.png"/>
</p>

6. Click Save on the bottom right.

#### Docker Hub
1. Go to [Docker Hub](https://hub.docker.com/)
2. Press "Continue with Google
3. Login to the **mhapy.noreply@gmail.com** with the password in the secrets txt file
4. You should be able to see all of the Docker images used in the project

<p align="center">
  <img src="/resources/mhapy_sentiment_docker_images.png"/>
</p>

Feel free to edit these however you'd like.


### Tokens and Credentials
To find the current tokens and credentials, navigate to the private AWS S3 bucket named "mhapy-sentiment-analysis" on your AWS account, and download the `sentiment_api_secrets.txt` it hosts all of the following tokens:

* AWS_ACCESS_KEY
* AWS_SECRET_ACCESS_KEY
* DB_HOST
* DB_NAME
* DB_PASSWORD
* DB_PORT
* DB_USER
* DOCKERHUB_TOKEN
* DOCKERHUB_USERNAME
* EC2_INSTANCE_IP
* TESTING_EC2_INSTANCE_IP
* SSH_PRIVATE_KEY

If you want to change any of our tokens or move to a new repository, be sure to modify or include these tokens.
> When changing or modifying the SSH_PRIVATE_KEY, include the header and footer "-----BEGIN RSA PRIVATE KEY-----" and "-----END RSA PRIVATE KEY-----" respectively.

This file also hosts the password credentials to the email address: ***mhapy.noreply@gmail.com***
This email address is who will send the warning message to the user. It is also linked to the Docker Hub account which hosts the Docker images that are deployed on the two EC2 instances. Be sure to sign in through Google in Docker Hub.
Feel free to modify, change, delete these accounts as you see fit.

The last item in the S3 bucket is the `mhapy-sentiment.pem` key which is crucial to SSH into both EC2 instances.

## Local Deployment
To set this up on your local machine/server, CD into your directory of choice on your local machine to set up the project. Ensure you have `Python` and `Node.js` installed beforehand. These instructions assumes you will be using **Ubuntu** bash.

### Clone the Project
```bash
$ git clone https://github.com/csc301-2023-fall/project-19-mhapy-t.git
```
Or use `GitHub Desktop` to clone a repository because of the new changes to password/tokens.

### Load in Envrionment Variables
```bash
$ export AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>
$ export AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>
$ export DB_HOST=<DB_HOST>
$ export DB_PORT=<DB_PORT>
$ export DB_NAME=<DB_NAME>
$ export DB_USER=<DB_USER>
$ export DB_PASSWORD=<DB_PASSWORD>
```
> Replace each of the assignments with the correct corresponding values hidden inside the txt file composed of all the tokens and secrets

### Install Packages and Run API using Docker
Build the containers and start running them using Docker Compose.
```bash
$ docker compose up -d --build
```
And now you have all three API files running, and can correctly call a POST request to the Node.js endpoints.

### Visit the Local Deployment
Go to http://localhost:4820 on your browser to call the POST request the same way as before or do this in terminal using **curl**
```bash
$ curl -X POST -H "Content-Type: application/json" -d '{"text":"Enter input text here", "user_id": "Enter user ID here", "time": "Enter ISO 8601 time here", "email": "Enter user email here"}' http://localhost:4820/analyze-sentiment > sentiment_graph.html
```
Or you can do this without the time property/field to set an automatic value:
```bash
$ curl -X POST -H "Content-Type: application/json" -d '{"text":"Enter input text here", "user_id": "Enter user ID here", "email": "Enter user email here"}' http://localhost:4820/analyze-sentiment > sentiment_graph.html
```
> You can also use this command to curl to the AWS deployed API above.

This will output the same HTML graph as the front end web version and will be redirected into a file named `sentiment_graph.html`. Open the HTML file to see the graph once again. 

### Shut Down Deployment
To shut down the server and all the API's run these commands.
```bash
$ docker compose stop
```
This will shut down the containers and can be restart with `docker compose up --build -d` again.

### Tests
Tests are automated through the test-node-flask.yml workflow already. If you want to run the tests manually on a local repository however, do these commands in this specific order. This assumes you have already pulled the git repository.
```bash
$ cd ml_model
$ pip install -r flask_requirements.txt
$ python3 test_sentiment_flask.py
$ cd ../graph_sentiment
$ pip install -r flask_requirements.txt
$ python3 test_graph_flask.py
$ cd ../node_api
$ npm install
$ npm test
```
