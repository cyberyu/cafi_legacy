
angular.module('projectServices',[]).factory('Project', function($resource){
    return $resource('/projects/:projectId', {projectId: '@id'}, {
        update: {
            method: 'PUT' // this method issues a PUT request
        }
    });
}).service('popupService',function($window){
    this.showPopup=function(message){
        return $window.confirm(message);
    }
});
