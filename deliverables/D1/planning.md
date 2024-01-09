# mhapy API/For All The Dogs
> _Note:_ This document will evolve throughout your project. You commit regularly to this file while working on the project (especially edits/additions/deletions to the _Highlights_ section). 
 > **This document will serve as a master plan between your team, your partner and your TA.**

## Product Details
 
#### Q1: What is the product?

   Our product is a sentiment analysis machine learning model trained on text data scraped from the mhapy app. 

   Partnered with mhapy, an online therapy solution, we address the challenge of underutilized text data collected from users of their app. Mhapy employs AI chatbots and personal journaling to assist users in managing their mental health. Users can interact with a chatbot for therapy sessions or use the app as a virtual journal. Both these offer a convenient solution to users seeking mental health solutions with anonymity and/or affordably. They also are planning to sell this app to other therapists to implement it within their website to better serve their clients using this digital solution.

   Since they have data that is not being used our solution involves building a text scraping API to extract data from both user prompts to the AI chatbot and personal journals. This data will be used to train a machine learning model capable of performing sentiment analysis. Once trained, the model will be integrated into an API, enabling real-time sentiment analysis of new text data from the app. Users can receive insights into whether their text is positive or negative and access scatter plot graphs displaying weekly trends. In cases of persistently negative trends, notifications can be sent to the user, an accountability buddy, or a therapist.

   Our goal is to help mhapy and their users better understand their mental well-being through data-driven insights, enhancing the overall effectiveness of the mhapy app in supporting their mental health. Overall, leading to a more impactful and helpful experience to their users.


Mockup Flow Diagram:

<p align="center">
  <img src="/deliverables/D1/resources/mockup.png" alt="Mockup Flow Diagram">
</p>

#### Q2: Who are your target users?

   Since our product is an API for a preexisting application, our target audience is technically the server in which our API is applied. Through this server, our end target users will be the company or mhapy themselves. The current users of the app will be mhapy’s end users, as in turn our end users will be theirs. So from our product patients who need a convenient solution to help with their mental health will be able to visually track their progress through the app to stay on track. As well as therapists of patients who can use this app for their clients and be notified if their client is using too much negative language. 


#### Q3: Why would your users choose your product? What are they using today to solve their problem/need?

   The user would choose our product if they want to be able to scrape data from their cloud database and use that data to train a machine learning model to perform prediction via sentiment on new data. With this, our API will be able to categorize text and display analytics showing useful trends to the user in terms of their negativity/positivity when it comes to writing text within the mhapy app. The API will also try to notify users periodically if they show a negative trend. More generally, this api is useful to a company who has a lot of underutilized data that wants to use that data to give a statistical analysis/visual using machine learning models. Specifically sentiment analysis.

   Currently they have nothing to solve this problem. They only have a therapist chatbot and personal journal for end users of the app to write their thoughts/feelings, but they are not utilizing it in an effective way to assist the end user. Thus our product is not only utilizing the data scraped from the app, but also implementing an entirely new functionality to it. That being, showing the users their texting trends within the app so they can be informed on their progress and improvements.
The creation of this API directly aligns with mhapy’s mission of making mental health resources more widely available for the general public as well as allows both users and therapists to make better use of the information which is already being input through the app.


#### Q4: What are the user stories that make up the Minumum Viable Product (MVP)?

The MVP is the process of retrieving data from the database, preprocessing, and training an ML model on it.

* As the server administrator, I want to securely connect to the cloud database so that I can view the text data that has been scraped from the mhapy app.
* As the server, I need to efficiently handle incoming POST requests from the mhapy app, enabling seamless data submission for sentiment analysis and ensuring a responsive and real-time analysis process
* As the server, I aim to extract the raw data from the database as the first step of data preprocessing, preparing it for subsequent cleaning and feature engineering steps to enhance the quality of the data.
* As the server, I intend to implement data cleaning procedures to eliminate noise and irrelevant information from the extracted user data. This cleaning step is crucial for optimizing the training process of our machine learning model. So that I can create a ML model that reduces the Bayes error to achieve optimal performance.
* As the server, my objective is to train a machine learning model on the preprocessed user data. This trained model will enable us to perform accurate sentiment analysis, providing valuable insights into the emotional content of user interactions within the mhapy app and ultimately enhancing the mental health support we offer.

Our partner hasn’t responded to our user stories yet, but we are planning to meet with him on Saturday and will get his feedback on them then.
Here is proof of us messaging them:
<p align="center">
  <img src="/deliverables/D1/resources/proof_of_q4.png" alt="Inquiry on Approval of User Stories">
</p>

**EDIT** Their response Saturday afternoon:
<p align="center">
  <img src="/deliverables/D1/resources/approval_q4.png" alt="Approval of User Stories">
</p>

#### Q5: Have you decided on how you will build it? Share what you know now or tell us the options you are considering.

   The specific tech stack for our project has not been exactly decided yet as our partner is open to any technologies. To build the text scraping API, we were thinking of using Node.js and Express.js to make it a RESTful API but are also open to Flask/Django. We are also open to making a GraphQL API and also possibly combining it with a WebSocket API to enable real time data transfer if our partner needs it. A possible option to test our API would be to use Postman. For actually scraping text if we were to use Node.js then libraries like Puppeteer and Cheerio would suffice otherwise BeautifulSoup for Python also works. To document our API, we’ll use Swagger and for authentication we’ll use the standard JWT for securing the endpoints.
   
   Our partner offered to use GCP (Google Cloud) or Microsoft Azure for the database to hold our text. By that extension, we were thinking of performing sentiment analysis using GCP or Azure’s NLP service. An alternative way for us to manually code the ML model through python with libraries and frameworks such as PyTorch, TensorFlow, Keras or even scikit-learn. For the database our partner decided to use a relational database, and they use PostgreSQL for their database. So we will probably use PostgreSQL as well. To deploy our API, we were thinking of hosting it on those same cloud services such as GCP or Azure. For the server runtime environment, we were considering using Node.js/Express.js since we would not need to use nginx/apache, but are open to using those instead of Express.js. To connect to the app, our partner said they will provide us with their own API’s to connect to the front end. For our architecture, since their app is already using the client-server pattern we will follow theirs, and contribute to the server as help fill in gaps in data transfer through APIs.


----
## Intellectual Property Confidentiality Agreement 
> Note this section is **not marked** but must be completed briefly if you have a partner. If you have any questions, please ask on Piazza.
>  
**By default, you own any work that you do as part of your coursework.** However, some partners may want you to keep the project confidential after the course is complete. As part of your first deliverable, you should discuss and agree upon an option with your partner. Examples include:
1. You can share the software and the code freely with anyone with or without a license, regardless of domain, for any use.
2. You can upload the code to GitHub or other similar publicly available domains.
3. You will only share the code under an open-source license with the partner but agree to not distribute it in any way to any other entity or individual. 
4. You will share the code under an open-source license and distribute it as you wish but only the partner can access the system deployed during the course.
5. You will only reference the work you did in your resume, interviews, etc. You agree to not share the code or software in any capacity with anyone unless your partner has agreed to it.

**Your partner cannot ask you to sign any legal agreements or documents pertaining to non-disclosure, confidentiality, IP ownership, etc.**

Briefly describe which option you have agreed to.

**Our partner decided option number 5 was the best for our IP Confidentiality Agreement.**

## Teamwork Details

#### Q6: Have you met with your team?

Yes! As a team, we played Skribbl.io, an online game where the team has to guess what one member is drawing before the time runs out. It was a good way to get to know each other and build our team’s connection.

<p align="center">
  <img src="/deliverables/D1/resources/team_bonding.png" alt="Skribbl Game">
</p>

Team Member Fun Facts:
* Patrick races in Triathlons.
* Hrid loves singing and writes his own music.
* Cole plays the saxophone
* Rowan plays the electric guitar and bass guitar.
* Umair likes swimming and playing soccer
* Jazli has over 1,000,000 XP for his Sniper Monkey on BTD6 

#### Q7: What are the roles & responsibilities on the team?


Team Leader / Partner Liaison / Software Engineer: Umair Hussain
* In charge of communicating with the partner and relaying information back to the team. Responsibilities include scheduling meetings with the partner on a weekly basis. Having a place to hold all the meeting questions from the group and the answers from the partner is created and held up to date. Additionally, as team leader I will encourage team members to communicate and provide frequent updates to ensure everyone is on the same page. I chose this role because I like to plan ahead and dislike when groups fail due to lack of communication. Additionally, I was the person to facilitate the first two meetings with the partner.
* As a software engineer I am in charge of helping with either the scraping and cleaning of the data or with the sentiment analysis side. My role is a more general software engineer and will be updated when we have a better idea of which area needs more help. I chose this role as I am interested in statistics and ML. Both the data preprocessing and training the model are both very important in this process and I would like an opportunity to utilize my skills in a real world scenario.

Web Scraper: Jazli Muhammad Khairi Leong
* My main responsibility is to scrape text from mhapy’s mobile app. Primarily off the journaling feature and to convert the text to a serialized format. I need to preserve this data on a database on a server to hand off to the sentiment analysis model. Using text scraping libraries such as Puppeteer or BeautifulSoup. This serves as the main backend portion of the code connecting the app to the server. I need to work with the Cloud Developer to host this API on a server which will be a cloud server. 
* I chose this role because I wanted to learn more about backend development such as Node.js/Express.js because I have not learned much about it. API’s are a core component of modern day software development and I wanted to understand how they work. Specifically, RESTful or GraphQL API’s and learning about WebSocket. How HTTP connections and as well as the rest of network infrastructure work in the contemporary era intrigue me.

Cloud Developer: Patrick Fidler
* In charge of writing the code for using existing cloud infrastructure, and creating new cloud infrastructure to store data we have processed. Some responsibilities include obtaining and filtering the application data stored on the Google Cloud, deploying infrastructure to host our API, and (maybe?) using cloud tools to send push notifications to relevant parties.

Machine Learning Engineer: Hrid Patel
* As a machine learning engineer, my primary responsibilities will revolve around developing and implementing the sentiment analysis machine learning model. Drawing on my recent experience in taking CSC311, I’ll utilize my knowledge of machine learning concepts and models to create an effective solution.
* I chose this role because of my recent exposure to machine learning in CSC311. The coursework provided me with strong foundational knowledge about the theory and implementation of various common machine learning models. I hope to be able to apply this knowledge to this real-world project and make a purposeful impact.

Data Visualization Engineer: Cole Wiltse
* I am responsible for the visual representation of the sentiment data recorded from our API. This means I have to be able to interpret and plot the sentiment data for each user and then send that graph to the user via the API. This graph may also have options to filter the data based on the range of time the user specifies.
* I chose this position because I have experience using Plotly in my first year at UofT. Though it has been a while since then, I am at least familiar with how to translate data into a visual medium and can make a meaningful contribution for our team.

Software / Machine Learning Engineer: Rowan Arora
* In charge of building the ML model which is trained and tested on the processed stored data. Responsibilities include building a functional and accurate neural network which can operate on mobile devices, and ensuring the neural network maintains accuracy on live end user data.
* The reason I chose this role is because in recent times I have been studying AI and Machine Learning, specifically neural networks, convolutional neural networks, hyperparameter tuning, regularization, and optimization, however, I have not had the chance to build an ML model on my own. My goal is to get a better understanding of AI/ML principles and implement my own AI/ML model through this project.


#### Q8: How will you work as a team?
  
   We plan to have weekly meetings, either over Discord or in-person, where we can discuss the current state of the project, possible issues we have run into, when we can schedule our partner meetings, and who is able to make it to said partner meetings.We also have a Discord group chat where we can discuss the project and hopefully come up with solutions to any of our problems. Finally, we have a Slack server with our partners where we can discuss any possible issues we have run into which we cannot solve and any questions we need the partner to answer. We plan to have weekly meetings with the partner on Saturday.
  
  
#### Q9: How will you organize your team?


   We are planning on using either Jira or Trello to keep our team organized and on track over the course of the semester. These tools include timelines, reports, schedules, and much more which we believe will be incredibly useful for keeping us organized. Also, we can easily include our TA and partner access to these systems, making them ideal tools for this project.
	
   We will prioritize tasks by the most recent due date and whether we need our partner involved in said task, meaning that we will try our best to complete tasks which are due the soonest, where the partner is directly involved before other tasks as to not have to contact our partner last minute and be unable to complete something.
	
   We will try to assign tasks amongst ourselves by strengths, which is to say if one member of the group is proficient in a specific framework, language, etc., they will most likely be the person assigned said task. However, this does not mean that they cannot contact the rest of the group for help. We will need to use APF (Adaptive Project Framework) since we will need to adapt to the client/partner’s changing demands.
Finally, we can keep track of the status of our work from inception to completion through the use of branching on GitHub as well as the aforementioned tools, Jira and Trello.


#### Q10: What are the rules regarding how your team works?

**Communications:**
 * To communicate between ourselves we use Discord.
 * We have a Slack channel that our partners gave to us and we use it to ask simple questions. We also have the opportunity to book a meeting with them via Google Meets to ask more in depth inquiries.

 
**Collaboration: (Share your responses to Q8 & Q9 from A1)**
 * The way we will ensure people are held accountable for attending meetings and completing action items is by constantly keeping in touch through our Discord group chat, which is to say that whenever a group member is working on something, running late to a meeting, or is struggling with completing their assigned tasks, they will make sure to message the group chat and let the rest of the group know what issues have arisen. As long as enough notice is given for a task a group member is running late on completing, the rest of us will be able to help out with the task. On top of this, whenever we complete a task, we will notify the group chat and check-off the box for said task on one of our organizational tools (Jira/Trello).
 * If one person does not contribute or is not responsive, we will first ensure that they are in fact alright (healthy/safe), and if they are alright, we will try our best to hold a meeting as a group to discuss how to address this issue. If the person is still unresponsive after all of this, we will schedule a meeting with our TA and try to figure out what next steps can be made in order to complete the project on time.

