// Karma configuration
// http://karma-runner.github.io/0.12/config/configuration-file.html
// Generated on 2015-06-09 using
// generator-karma 1.0.0

module.exports = function(config) {
  'use strict';

  config.set({
    // enable / disable watching file and executing tests whenever any file changes
    autoWatch: true,

    // base path, that will be used to resolve files and exclude
    basePath: '../',

    // testing framework to use (jasmine/mocha/qunit/...)
    // as well as any additional frameworks (requirejs/chai/sinon/...)
    frameworks: [
      "jasmine"
    ],

    // list of files / patterns to load in the browser
    files: [
        'src/vendor/angular/angular.js',            
        'src/vendor/angular-mocks/angular-mocks.js',
        'src/vendor/lodash/lodash.min.js',
        'src/vendor/jasmine-object-matchers/dist/jasmine-object-matchers.min.js',
        'src/vendor/jquery/dist/jquery.js',
        'src/vendor/jquery.easing/js/jquery.easing.js',
        'src/vendor/cf-*/src/js/*.js',
        'src/vendor/d3/d3.min.js',
        'src/vendor/angular/angular.min.js',
        'src/vendor/cf-expandables/src/js/cf-expandables.js',
        'src/vendor/angular-sanitize/angular-sanitize.min.js',
        'src/vendor/elasticsearch/elasticsearch.angular.min.js',
        'src/vendor/pikaday/pikaday.js',
        'src/vendor/moment/min/moment.min.js',
        'src/vendor/elastic.js/dist/elastic.min.js',
        'src/vendor/angular-bootstrap/ui-bootstrap-tpls.min.js',
        'src/vendor/nya-bootstrap-select/dist/js/nya-bs-select.min.js',
        'src/static/js/annotated/app-annotated.js',
        'src/static/js/annotated/app-controller-annotated.js',
        'src/static/js/annotated/chartFilter-annotated.js',
        'src/static/js/annotated/dateInput-annotated.js',
        'src/static/js/annotated/pillFilter-annotated.js',
        'src/static/js/annotated/client-service-annotated.js',
        'src/static/js/annotated/export-service-annotated.js',
        'src/static/js/annotated/suggest-service-annotated.js',
        'src/static/js/annotated/save-search-service-annotated.js',
        'test/app-spec.js',
        'test/chartFilter-spec.js',
        'test/saveService.spec.js',
        'test/modal-spec.js',
        'test/pillFilter-spec.js'
    ],

    // coverage reporter generates the coverage
    reporters: ['progress', 'coverage'],

    preprocessors: {
      // source files, that you wanna generate coverage for
      // do not include tests or libraries
      // (these files will be instrumented by Istanbul)
      'src/static/js/**/*.js': ['coverage']
    },

    // list of files / patterns to exclude
    exclude: [
      ""
    ],

    // web server port
    port: 8282,

    // Start these browsers, currently available:
    // - Chrome
    // - ChromeCanary
    // - Firefox
    // - Opera
    // - Safari (only Mac)
    // - PhantomJS
    // - IE (only Windows)
    browsers: [
      "PhantomJS"
    ],

    // Which plugins to enable
    plugins: [
      "karma-phantomjs-launcher",
      "karma-jasmine",
      "karma-coverage"
    ],

    // Continuous Integration mode
    // if true, it capture browsers, run tests and exit
    singleRun: false,

    colors: true,

    // level of logging
    // possible values: LOG_DISABLE || LOG_ERROR || LOG_WARN || LOG_INFO || LOG_DEBUG
    logLevel: config.LOG_DEBUG,

    // Uncomment the following lines if you are using grunt's server to run the tests
    // proxies: {
    //   '/': 'http://localhost:9000/'
    // },
    // URL root prevent conflicts with the site root
    // urlRoot: '_karma_'
  });
};
