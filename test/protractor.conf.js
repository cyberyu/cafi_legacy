exports.config = {
  seleniumAddress: 'http://localhost:4444/wd/hub',
  specs: ['search.spec.js', 'result.spec.js'],

  onPrepare: function() {
    // browser.ignoreSynchronization = true;
    browser.driver.get('http://localhost:8081/login');

    browser.driver.findElement(by.css('[name=username]')).sendKeys('protractor');
    browser.driver.findElement(by.css('[name=password]')).sendKeys('Testing123');
    browser.driver.findElement(by.css('[value="Sign In"]')).click();

    // Login takes some time, so wait until it's done.
    // For the test app's login, we know it's done when it redirects to
    // index.html.
    return browser.driver.wait(function() {
      return browser.driver.getCurrentUrl();
    }, 3000);
  }
};