angular.module('projectServices', []).factory('Project', function ($resource) {
  return $resource('/api/projects/:projectId', {projectId: '@id'}, {
    update: {method: 'PUT'},
    get: {
      method: 'GET',
      isArray: false,
      transformResponse: function(data) {
          return angular.fromJson(data);
      }
    },
    query: {
      method: 'GET',
      isArray: true
      //transformResponse: function(data) {
      //    return angular.fromJson(data).results;
      //}
    }
  });
}).service('popupService', function ($window) {
  this.showPopup = function (message) {
    return $window.confirm(message);
  }
}).factory('GeoSearch', function ($resource) {
  return $resource('/api/geosearch/:gsearchId', {gocId: '@id'}, {
    query: {
      method: 'GET',
      //isArray: true
      transformResponse: function(data) {
        return angular.fromJson(data);
      }
    }
  });
});

angular.module('projectServices').factory('Search', function($resource){
  return $resource('/api/gsearch/:gsearchId', {gsearchId: '@id'}, {
    update: {method: 'PATCH'},
    query: {method: 'GET', isArray: false}
  })
});

angular.module('projectServices').factory('Gdoc', function ($resource) {
  return $resource('/api/gdocs/:gdocId', {gdocId: '@id'}, {
    update: {method: 'PATCH'},
    query: {method: 'GET', isArray: false}
  });
});

angular.module('projectServices').factory('Company', function ($resource) {
  return $resource('/api/companies/:companyId', {companyId: '@id'}, {
    update: {method: 'PUT'},
  });
});

angular.module('projectServices').factory('Risk', function ($resource) {
  return $resource('/api/risks/:riskId', {riskId: '@id'}, {
    update: {method: 'PUT'},
    get: {method: 'GET',
      transformResponse: function(data) {
        return angular.fromJson(data);
      }
    }
  });
});

angular.module('projectServices').factory('PredefinedSearch', function ($resource) {
  return $resource('/api/predefined_searchs/:id', {id: '@id'}, {
    update: {method: 'PUT'},
    get: {method: 'GET',
      transformResponse: function(data) {
        return angular.fromJson(data);
      }
    }
  });
});


angular.module('projectServices').factory('RiskItem', function ($resource) {
  return $resource('/api/risk_items/:riskItemId', {riskItemId: '@id'}, {
    update: {method: 'PUT'}
  });
});

angular.module('projectServices').factory('Relation', function ($resource) {
  return $resource('/api/relations/:id', {id: '@id'}, {
    update: {method: 'PUT'}
  });
});
