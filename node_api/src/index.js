const express = require('express');
const fs = require('fs');
const server = express();
const AWS = require('aws-sdk');
const axios = require('axios');
const bodyParser = require('body-parser');
const cors = require('cors');
const nodemailer = require('nodemailer');
const yaml = require('js-yaml')
const { specs, swaggerUi } = require('./swagger');


AWS.config.update({
  accessKeyId: process.env.AWS_ACCESS_KEY_ID,
  secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  region: 'us-east-1',
});

const emailYaml = fs.readFileSync('./config/low_sentiment_email.yaml', 'utf8');
const emailInfo = yaml.load(emailYaml);

const s3 = new AWS.S3();
const bucketName = 'mhapy-sentiment-analysis';
const journalKey = 'sentiment_journal_text.json';

server.use(bodyParser.json());

server.use(cors());

server.use('/api-docs', swaggerUi.serve, swaggerUi.setup(specs));

server.use(bodyParser.urlencoded({ extended: true }));

server.use(express.static('public'));

const isDockerEnvironment = process.env.DOCKER === 'true';

server.get('/journal-text', async (req, res) => {
  const params = {
    Bucket: bucketName,
    Key: journalKey,
  };
  
  try {
    const journalTextData = await s3.getObject(params).promise();

    const jsonData = JSON.parse(journalTextData.Body.toString());

    jsonData.forEach(entry => {
      entry.text = entry.text.replace(/\n/g, ' ').replace(/,/g, '');
    });

    const csvContent = [
      ['text', 'sentiment'], // CSV header
      ...jsonData.map(entry => [entry.text, entry.sentiment]),
    ].map(row => row.join(',')).join('\n');

    // Send CSV as response
    res.header('Content-Type', 'text/csv');
    res.attachment('sentiment_journal_text.csv');
    res.status(200).send(csvContent);
  } catch (error) {
    console.error('Error:', error);
    if (error.code === 'NoSuchKey') {
      res.status(404).json({ error: 'Key resource not found' });
    } else {
      res.status(500).json({ error: 'Internal Server Error' });
    }
  }
});

server.get('/test', async (req, res) => {
  try {
    const random = Math.random();
    let message;

    message = "Example test json to confirm API is running and returns an random number";
    res.status(200).send({ message, randomNumber: random });
    
  } catch (error) {
    console.error('Error:', error.message);
    res.status(500).send({ error: "Internal Server Error" });
  }
});

server.get('/scrape-text', async (req, res) => {
  try {
    // Given endpoint to scrape data
    const response = await axios.get('https://mahppy-apis.nn.r.appspot.com/api/v1/get_all_journal_text');

    const journalTextData = response.data.map(item => ({
      text: item.text,
      id: item.user.id,
      date_created: item.date_created,
      email: item.user.email
    }));

    // Convert the data to a JSON-formatted string
    const jsonString = JSON.stringify(journalTextData, null, 2); 

    const filePath = 'journal_text.json';

    // Write the data to the file
    fs.writeFileSync(filePath, jsonString);

    res.status(200).download(filePath, 'journal_text.json', (err) => {
      if (err) {
        console.error('Error:', err);
        res.status(500).send("Error: Couldn't download the journal text json file");
      } else {
        console.log('File sent successfully');
        fs.unlinkSync(filePath);
      }
    });

  } catch (error) {
    console.error('Error:', error.message);
    if (error.response) {
      if (error.response.status === 404) {
        res.status(404).json({ error: 'Data not found' });
      } else {
        res.status(500).json({ error: 'Internal Server Error' });
      }
    } else {
      res.status(500).json({ error: 'Internal Server Error' });
    }
  } 
});

server.post('/retrieve-graph', async (req, res) => {
  try {
    const userIdData = req.body.user_id;
    if (userIdData == null || userIdData === "") {
      return res.status(400).json({ error: 'Bad request, missing or invalid parameter for user_id' });
    }
  
    let graphEndpoint = isDockerEnvironment ? 'http://mhapy-graph-container:5001/get-graph' : 'http://localhost:5001/get-graph';
  
    const graphResponse = await axios.post(graphEndpoint, {
      user_id: userIdData
    });
    if (graphResponse.status === 200) {
      const graphHtml = graphResponse.data.graph_html;
      return res.status(200).send(graphHtml);
    } else {
      const errorMessage = graphResponse.data.error || 'Failed to retrieve a graph from database';
      return res.status(graphResponse.status).json({ error: errorMessage });
    }

  } catch (error) {
    console.error('Error fetching data:', error);
    res.status(500).json({ error: 'Failed to fetch data' });
  }
});  

server.post('/analyze-sentiment', async (req, res) => {
  try {
    const textData = req.body.text;
    const userIdData = req.body.user_id;
    const emailData = req.body.email;

    let timeData = req.body.time;
    // Temporary current time for timeData if no time given
    if (timeData == null || timeData == ""){
      const currentDate = new Date();
      timeData = currentDate.toISOString();
    }
    const iso8601Regex = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z$/;

    if (!iso8601Regex.test(timeData)) {
      // Return a 404 response code and an error message
      const errorMessage = "Time data inputted is not in ISO 8601 format";
      return res.status(400).send(errorMessage);
    }

    if (!textData || !userIdData) {
      // If any required parameters are missing, return a 400 response
      return res.status(400).json({ error: 'Bad request, missing or invalid parameters text or user_id' });
    }
    let sentimentEndpoint;
    if (isDockerEnvironment){
      sentimentEndpoint = 'http://mhapy-ml-container:5005/compute-sentiment';
    }
    else {
      sentimentEndpoint = 'http://localhost:5005/compute-sentiment';
    }

    // Make a POST request to Sentiment Flask 
    const sentimentResponse = await axios.post(sentimentEndpoint, { text: textData });
    
    if (sentimentResponse.status !== 200) {
      // If the sentiment analysis request fails, return a 500 response
      return res.status(500).json({ error: 'Failed to perform sentiment analysis' });
    }

    if (sentimentResponse.data.prediction === 1 && sentimentResponse.data.probability > 95) {
      // Send warning email to the provided emailData
      await sendWarningEmail(emailData);
    }

    let insertEndpoint;

    if (isDockerEnvironment){
      insertEndpoint = 'http://mhapy-ml-container:5005/update-database';
    }
    else {
      insertEndpoint = 'http://localhost:5005/update-database';
    }
    const insertResponse = await axios.post(insertEndpoint, { 
      text: textData , 
      user_id: userIdData, 
      time: timeData, 
      sentiment: sentimentResponse.data.prediction, 
      score: sentimentResponse.data.probability
    });

    if (insertResponse.status !== 200) {
      // If the sentiment analysis request fails, return a 500 response
      return res.status(500).json({ error: 'Failed to update database' });
    }

    let graphEndpoint
    if (isDockerEnvironment){
      graphEndpoint = 'http://mhapy-graph-container:5001/get-graph';
    }
    else {
      graphEndpoint = 'http://localhost:5001/get-graph';
    }

    const graphResponse = await axios.post(graphEndpoint, { user_id: userIdData } );

    if (graphResponse.status !== 200) {
      // If the graph generation request fails, return a 500 response
      return res.status(500).json({ error: 'Failed to generate graph' });
    }
    
    const graphHtml = graphResponse.data.graph_html;

    // Send the HTML as a response
    res.status(200).send(graphHtml);    
    
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});



async function sendWarningEmail(email) {

  let transporter = nodemailer.createTransport({
    host: 'smtp-relay.sendinblue.com',
    port: 587,
    secure: false, 
    auth: {
      user: 'mhapy.noreply@gmail.com', // Sendinblue login
      pass: 'Ia9mEqnD5VYUHyQw' // Sendinblue password
    }
  });

  let mailOptions = {
    from: emailInfo.from,
    to: email,
    subject: emailInfo.subject,
    text: emailInfo.body
  };

  try {
    // Send email
    let info = await transporter.sendMail(mailOptions);
    console.log('Email sent: ', info.response);
  } catch (err) {
    console.error('Error occurred while sending email: ', err);
  }
}

const port = 4820;
server.listen(
    port,
    () => {
  console.log(`Server is listening on port ${port}`);
});

module.exports = server;

// Handle application exit and close the server
process.on('exit', async () => {
  console.log('Connection to the sentiment analysis API has been closed.');
});

// Handle Ctrl+C (SIGINT) to gracefully close server endpoints
process.on('SIGINT', async () => {
  console.log('Connection to the sentiment analysis API is closing.');
  process.exit(0);
});

