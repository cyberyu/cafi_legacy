The Consumer Complaints application uses JavaScript-based end to end and unit testing to cover most of the application.  The application uses Protractor to run end to end browser tests, and Karma to run unit tests.

## Dependencies
1. Node.js and NPM
2. Protractor
3. Java JDK for Webdriver / Selenium (or a SauceLabs tunnel) - on CFPB laptops this means requesting access to the install package via Self-Service if not already installed

## Installing Protractor and starting Selenium:
* `npm install -g protractor` - Installs protractor
* `webdriver-manager update` - Updates Selenium for Tests
* `webdriver-manager start` - Starts the Selenium Server

## Test Setup for Complaints Search
Tests are located in the /test directory at the top level of the application.

Run `protractor protractor.conf.js` to initiate the tests.

Any updates to tests or additional specs should be added to the conf file and submitted via pull requests.

Further documentation about each tool can be found on their respective sites:
* [Protractor](https://angular.github.io/protractor/#/)
* [Karma](http://karma-runner.github.io/0.13/index.html)
* [Jasmine](http://jasmine.github.io/2.3/introduction.html)