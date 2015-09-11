CAFI Automation Tool
===========
## Description 
The CAFI Automation Tool uses ElasticSearch, Django, and a JavaScript/Angular frontend to allow CAFI team to perform supply chain risk research easier. 

## Getting Started

### System Requirements

### Setting Up

see instruction [here](https://gitlab.com/nkvitamine/cafi/wikis/how-to-set-up-dev-server)

### Design

### Data

#### Index

## Technology Decisions

### Backend

* Django
  * Django REST Framework
* PostgreSQL
* ElasticSearch
* Redis for caching 
* RabbitMQ for message queue 
* Celery for distributed processing

### Frontend
The frontend technology was selected after an evaluation of various JavaScript frameworks including React.js, jQuery, and others. Angular was selected because of existing tooling built for elasticsearch including the Angular browser build from elastic.co (official, but beta), as well as tooling like ElasticUI which provided a means to quickly build tracer versions of the search app to minimize downstream risk for our technology decisions. 
Further, Angular provides a full end-to-end test suite with Karma and Protractor that are quite easy to use and do not require complex frameworks such as behave. As a result, our entire front-end is written in JavaScript including tests, and the front-end can be ported out of our Django wrapper to be used for other applications if advantageous.

* AngularJS with ElasticSearch.js Angular browser build
* Foundation Framework for CSS styling
* Karma / Jasmine / Protractor Test Suite
* Grunt for build and test management
* Bower for dependency management


## Developers

## How to test the software
To view testing instructions for the codebase, please see the README.md in the `/test` folder.

## Known issues

None

## Getting help

If you have questions, concerns, bug reports, etc, please file an issue in this repository's Issue Tracker.

## Getting involved

Please see our [CONTRIBUTING](CONTRIBUTING.md) file for more information about contributing

## Troubleshooting  

