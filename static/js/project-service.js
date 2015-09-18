angular.module('projectServices', []).factory('Project', function ($resource) {
    return $resource('/api/projects/:projectId', {projectId: '@id'}, {
        update: {method: 'PUT'},
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
});
