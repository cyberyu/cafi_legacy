
// Service
//
// esFactory() creates a configured client instance. Turn that instance
// into a service so that it can be required by other parts of the application

// IE doesn't support Origin so we shim it below
if (!window.location.origin) {
  window.location.origin = window.location.protocol + "//" + window.location.hostname + (window.location.port ? ':' + window.location.port: '');
}

var esLocation = window.location.origin;

SearchApp.service('client', function (esFactory) {
  return esFactory({
    host: esLocation,
    apiVersion: '1.5',
    log: 'trace'
  });
});