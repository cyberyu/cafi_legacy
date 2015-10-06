angular.module('projectServices', []).factory('Project', function ($resource) {
    return $resource('/api/projects/:projectId', {projectId: '@id'}, {
        update: {method: 'PUT'},
        get: {
            method: 'GET',
            //transformResponse: function(data) {
            //    return angular.fromJson(data).results[0];
            //}
        },
        query: {
            method: 'GET',
            isArray: true,
            //transformResponse: function(data) {
            //    return angular.fromJson(data).results;
            //}
        }
    });
}).service('popupService', function ($window) {
    this.showPopup = function (message) {
        return $window.confirm(message);
    }
}).factory('Search', function ($resource) {
    return $resource('/api/gsearch/:searchId', {searchId: '@id'}, {
        query: {
            method: 'GET',
            isArray: true,
            transformResponse: function(data) {
                return angular.fromJson(data).results;
            }
        }
    });
}).factory('Gdoc', function ($resource) {
    return $resource('/api/gdocs/:gocId', {gocId: '@id'}, {
        query: {
            method: 'GET',
            isArray: true,
            transformResponse: function(data) {
                return angular.fromJson(data).results;
            }
        }
    });
}).factory('GeoSearch', function ($resource) {
    return $resource('/api/geosearch/:gsearchId', {gocId: '@id'}, {
        query: {
            method: 'GET',
            isArray: true,
            transformResponse: function(data) {
                return angular.fromJson(data).results;
            }
        }
    });
}).factory('GeoSearchResult', function ($resource) {
    return $resource('/api/geosearchresult/:geosearchresultId', {gocId: '@id'}, {
        query: {
            method: 'GET',
            isArray: true,
            transformResponse: function(data) {
                return angular.fromJson(data).results;
            }
        }
    });
});
