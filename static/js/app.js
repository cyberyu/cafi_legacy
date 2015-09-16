'use strict';

var cafiApp = angular.module('cafiApp', [
	// 'elasticsearch',
	'ngSanitize',
	'ngResource',
	'ngRoute',
	// 'ui.bootstrap',
	// 'nya.bootstrap.select',
	'projectControllers',
	'projectServices'
]);

cafiApp.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

cafiApp.config(['$routeProvider',
  function($routeProvider) {
	$routeProvider.when('/projects', {
        controller: 'ProjectListCtrl',
        templateUrl: '/static/partials/project_list.html'
      }).when('/projects/new', {
        controller: 'ProjectCreateCtrl',
        templateUrl: '/static/partials/project_add.html'
      }).when('/', {
      	controller: 'loginCtrl',
      	templateUrl: '/static/partials/register.html'
      }).otherwise({
        redirectTo: '/projects'
      });
  }]);
