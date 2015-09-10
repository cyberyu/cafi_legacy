exports.config = {
  specs:        ['search.spec.js', 'result.spec.js'],
  capabilities: {
    browserName:         'chrome',
    name:                'cr-search-browser-tests ' + process.env.SITE_DESC,
    'tunnel-identifier': process.env.SAUCE_TUNNEL
  },

  sauceUser: process.env.SAUCE_USER,
  sauceKey:  process.env.SAUCE_KEY,

  onPrepare: function() {
    browser.driver.get('http://crsearch.demo.cfpb.gov/login/');
    browser.driver.findElement(by.css('[name=username]')).sendKeys('protractor');
    browser.driver.findElement(by.css('[name=password]')).sendKeys('Testing123');
    browser.driver.findElement(by.css('[value="Sign In"]')).click();

    return browser.driver.wait(function() {
      return browser.driver.getCurrentUrl();
    }, 3000);
  }
};