'use strict';

var projectControllers = angular.module('projectControllers', []);

var cafiApp = angular.module('cafiApp', [
  // 'elasticsearch',
  'ngSanitize',
  'ngResource',
  'ngRoute',
  'ngCsvImport',
  'ngCsv',
  'ngCookies',
  'ngTagsInput',
  'ng-mfb',
  'ui.bootstrap',
  'uiGmapgoogle-maps',
  'smart-table',
  'ngFileUpload',
  'bw.paging',
  'angular-highlight',
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
    }).when('/projects/:id/google', {
      controller: 'GoogleSearchCtrl',
      templateUrl: '/static/partials/_gsearch.html'
    }).when('/projects/:id/geo', {
      controller: 'GeoSearchCtrl',
      templateUrl: '/static/partials/_geosearch.html'
    }).when('/projects/:id', {
      controller: 'ProjectBoardCtrl',
      templateUrl: '/static/partials/project_board.html'
    }).otherwise({
      redirectTo: '/projects'
    })
  }]).config(function(uiGmapGoogleMapApiProvider) {
  uiGmapGoogleMapApiProvider.configure({
    libraries: 'weather,geometry,visualization'
  });
});

cafiApp.factory('myHttpInterceptor', ['$q','$location', '$rootScope', function ($q, $location, $rootScope) {
    return {
        response: function (response) {
          return response;
        },
        responseError: function (response) {
          $rootScope.needLogin = true;
          $location.path('/');
          return $q.reject(response);
        }
    };
}]);

cafiApp.config(function ($httpProvider) {
    $httpProvider.interceptors.push('myHttpInterceptor');
});