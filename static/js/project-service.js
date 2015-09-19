angular.module('projectServices', []).factory('Project', function ($resource) {
    return $resource('/api/projects/:projectId', {projectId: '@id'}, {
        update: {method: 'PUT'},
        get: {
            method: 'GET',
            transformResponse: function(data) {
                return angular.fromJson(data).results[0];
            }
        },
        query: {
            method: 'GET',
            isArray: true,
            transformResponse: function(data) {
                return angular.fromJson(data).results;
            }
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
    return $resource('/api/gdocs/:gocId', {searchId: '@id'}, {
        query: {
            method: 'GET',
            isArray: true,
            transformResponse: function(data) {
                return angular.fromJson(data).results;
            }
        }
    });
});
