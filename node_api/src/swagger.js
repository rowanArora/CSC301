const swaggerUi = require('swagger-ui-express');
const YAML = require('js-yaml');
const fs = require('fs');

// Load the Swagger YAML file
const swaggerYaml = fs.readFileSync('./docs/node_swagger.yaml', 'utf8');
const specs = YAML.load(swaggerYaml);

module.exports = { specs, swaggerUi };
