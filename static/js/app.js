'use strict';

var cafiApp = angular.module('cafiApp', [
    // 'elasticsearch',
    'ngSanitize',
    'ngResource',
    'ngRoute',
    'ngCsvImport',
    'ngCsv',
    'ui.bootstrap',
    // 'nya.bootstrap.select',
    'projectControllers',
    'projectServices']);

cafiApp.config(['$httpProvider', function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

cafiApp.config(['$routeProvider',
    function ($routeProvider) {
        $routeProvider.when('/projects', {
            controller: 'ProjectListCtrl',
            templateUrl: '/static/partials/project_list.html'
        }).when('/', {
            controller: 'loginCtrl',
            templateUrl: '/static/partials/register.html'
        }).when('/projects/:id', {
            controller: 'ProjectBoardCtrl',
            templateUrl: '/static/partials/project_board.html'
        }).otherwise({
            redirectTo: '/projects'
        });
    }]);
