# mhapy API/For All The Dogs
## Partner Intro
 * **Partner Organization**: mhapy
 * **Contact**: Chijindu Ukagwu
 * **Email**: chijinduukagwu@gmail.com
 * **Title**: Founder
 * mhapy is an online therapy solution that utilizes AI chatbots and personal journaling to assist users in managing their mental health. The app offers users the opportunity to communicate with a chatbot for therapy and maintain personal journals to record their thoughts and feelings.

## Project Description
 * Our project aims to enhance the mhapy app by providing an API that enables sentiment analysis of user-generated text data. The API will scrape data from both user prompts to the AI chatbot and personal journals, allowing us to train a machine learning model for sentiment analysis.
 * This model will categorize text as positive or negative, allowing us to visualize the data in a user friendly graph that will be sent back to the user. If a negative trend is detected, notifications can also be sent to the user, an accountability buddy, or a therapist.
​
### MVP
Scrape journal text data from mhapy app of their text, user ID, timestamp and email. Confirmed by our partner. 

## Key Features/User Stories
Each user story will be from the perspective of the mhapy backend API.
### 1. Text Scraping 
 * As the mhapy backend API, I want to gather journal text data to train a sentiment analysis model on.
 * Our created API allows users to scrape text data from the mhapy app database which includes prompts to their journal text.
### 2. Sentiment Analysis
 * As the mhapy backend API, I want to analyze the sentiment of a given user's text.
 * The API includes a sentiment analysis LSTM ML model that categorizes text data as either positive or negative, with a score associated with it, providing insights into the user's emotional state.
### 3. Trend Analytics
 * As the mhapy backend API, I want to give back a visualized version of a user's sentiment.
 * API sends back user a line graph showing trends in their sentiment data over time, helping them gain a better understanding of their emotional patterns over time.
### 4. Automated Notifications
 * As the backend API, I want to detect and also help/warn users if they might be having mental health issues. 
 * The API can send an email notification to user if an extreme negative sentiment is detected in the user's text data, ensuring timely support and intervention.
​
## Demo
Here is a link to a video demonstration of how to use the API, which also includes a quick demo of how to integrate it into your backend API.
https://youtu.be/bBYTjkQpiDI

For information on the creation of this project and how to continue development, visit the **development_information.md** file which has more in depth details about the project.

## Instructions

### Sentiment Analysis & Trend Analaytics:
1. Visit this link: http://ec2-54-165-193-93.compute-1.amazonaws.com:4820/ or if that doesn't work use this link: http://54.165.193.93:4820/
2. You will see a basic front end to send a POST request to two endpoints in two respective boxes: 

<p align="center">
  <img src="/resources/front_end_simulate_request.png"/>
</p>

The box on the left will simulate a POST request to /analyze-sentiment to analyze a sentiment of a text from a given user and has four text fields:
* **Text** to analyze the sentiment
* **User ID** of who the text is from
* **Time** that it was sent to the database
* **Email** of the user who submitted the text

For the **Time** text field, it needs to be in **ISO 8601** format (2023-04-12 10:36:22.423), but if the field is left empty it will automatically get the current time. So when testing it's easier if you leave it empty. 

The box on the right will simulate a POST request to /retrieve-graph which will retrieve a graph of the given users' recorded sentiment values and has one text field:
* **User ID** of any user in the database

3. Press the Analyze Sentiment button at the bottom of the left box to see a graph plotting the sentiment of that inputted text with its score/confidence or the Retrieve Graph button at the bottom of the right box and you will see a plot of the recorded sentiments of text the user submitted.
> Note: To get more negative outputs through the /analyze-sentiment endpoint, try to use more extreme mental health keywords such as "death, suicide, self harm, lonely, depressed".

4. If you'd like to see more points on the graph, visit back the same link: http://ec2-54-165-193-93.compute-1.amazonaws.com:4820/

   Repeat the same process for the /analyze-sentiment endpoint to enter new text for the **same** user, it will give you back a graph with the previous sentiment you inputted from before along with the new text sentiment.

### Text Scraping
1. Visit the /scrape-text endpoint:
   
   http://ec2-54-165-193-93.compute-1.amazonaws.com:4820/scrape-text or http://54.165.193.93:4820/scrape-text 
3. You should be downloading file called journal_text.json which contains all of the journal text from mhapy's API off their database
4. Right click on the file and open with Notepad, TextEdit, VSCode or your favourite text editor to inspect the contents.

---
The testing/staging environment link is also available here:

http://ec2-54-210-145-50.compute-1.amazonaws.com:4820 with the same functionalities.

---

### Documentation
In replacement of UX requirements, since our project is an API, visit our Swagger Documentation links to view a presentation of the API:

[Node.js API Swagger Documentation](http://ec2-54-165-193-93.compute-1.amazonaws.com:4820/api-docs/)

[Sentiment Flask API Swagger Documentation](http://ec2-54-165-193-93.compute-1.amazonaws.com:5005/apidocs/)

[Graph Flask API Swagger Documentation](http://ec2-54-165-193-93.compute-1.amazonaws.com:5001/apidocs/)

## Coding Standards and Guidelines
Key guidelines include limited use of globals, standard headers for modules, and naming conventions for variables, constants, and functions. Proper indentation is emphasized, and error return values are specified for functions encountering an error condition. We prioritize readability, proper documentation, and avoiding overly complex or lengthy functions.
​
## Licenses 
We are using a proprietary all rights reserved license because our partner requested that the code to not be shared with others and for it to be private.
It won't have much effect on our development since all of the other code that we are connecting to is already private within our partners' repositories or we would just be connecting to it via an endpoint. 
