const request = require('supertest');
const { expect } = require('chai');
const nock = require('nock');
const server = require('../src/index');

describe('GET /scrape-text', () => {
    it('should scrape text and respond with a downloadable JSON file', (done) => {
        request(server)
            .get('/scrape-text')
            .expect(200)
            .expect((response) => {
                const contentType = response.headers['content-type'];
                expect(contentType.includes('application/json')).to.be.true;
            })
            .end((err, response) => {
                if (err) {
                    done(err);
                    return;
                }
                
                done();
            });
    }).timeout(6000);;
});

describe('POST /analyze-sentiment', () => {
    before(() => {
      // Mocking the sentiment analysis endpoint
      nock('http://localhost:5005')
        .post('/compute-sentiment')
        .reply(200, {
          prediction: 1,
          probability: 0.75
        });
  
      // Mocking the update database endpoint
      nock('http://localhost:5005')
        .post('/update-database')
        .reply(200, {
          status: 'success'
        });
  
      // Mocking the graph generation endpoint
      nock('http://localhost:5001')
        .post('/get-graph')
        .reply(200, {
          graph_html: '<div>Mocked Graph HTML</div>'
        });
    });
  
    it('should analyze sentiment and generate graph HTML', async () => {
      // Your test code that makes the request to /analyze-sentiment using supertest or similar
  
      const requestBody = {
        text: 'I am so very happy right now',
        user_id: 'Node.js Test User'
        // Add other necessary properties like time if needed
      };
  
      const response = await request(server)
        .post('/analyze-sentiment')
        .send(requestBody);
  
      // Assertions based on the response received from the /analyze-sentiment endpoint
      // For example, you can check if the response contains the expected HTML
      expect(response.status).to.equal(200);
      expect(response.text).to.contain('<div>Mocked Graph HTML</div>');
    });
  });


describe('GET /test', () => {
    it('should return a JSON response with a message and a random number', (done) => {
        request(server)
            .get('/test')
            .expect(200)
            .expect('Content-Type', /json/)
            .end((err, response) => {
                if (err) {
                    done(err); // Signal test failure and pass the error to Mocha
                    return;
                }

                expect(response.body).to.have.property('message').that.is.a('string');
                expect(response.body).to.have.property('randomNumber').that.is.a('number');

                done(); // Signal test completion

            });
    });
});



describe('POST /retrieve-graph', () => {
  before(() => {
    const userId = 'valid_user_id';
    const graphHtml = '<div>Mocked Graph HTML</div>';

    nock('http://localhost:5001')
      .post('/get-graph', { user_id: userId })
      .reply(200, { graph_html: graphHtml });

    const invalidUserId = null;
    nock('http://localhost:5001')
      .post('/get-graph', { user_id: invalidUserId })
      .reply(400, { error: 'User ID is invalid' });
  });

  it('should retrieve a graph HTML for a valid user_id', async () => {
    const userId = 'valid_user_id';
    const graphHtml = '<div>Mocked Graph HTML</div>';

    const response = await request(server)
      .post('/retrieve-graph')
      .send({ user_id: userId });

    expect(response.status).to.equal(200);
    expect(response.text).to.equal(graphHtml);
  });

  it('should handle missing or invalid user_id and return a 400 error', async () => {
    const invalidUserId = null;

    const response = await request(server)
      .post('/retrieve-graph')
      .send({ user_id: invalidUserId });

    expect(response.status).to.equal(400);
    expect(response.body).to.deep.equal({ error: 'Bad request, missing or invalid parameter for user_id' });
  });
});



describe('GET /journal-text', () => {
    it('should respond with a CSV file containing journal text data', (done) => {
        request(server)
            .get('/journal-text')
            .expect(200)
            .expect('Content-Type', 'text/csv; charset=utf-8')
            .expect((response) => {
                const contentType = response.headers['content-type'];
                expect(contentType.includes('text/csv')).to.be.true;
            })
            .end((err, response) => {
                if (err) {
                    done(err);
                    return;
                }
                done();
                process.kill(process.pid, 'SIGINT');
            });
    });
});

