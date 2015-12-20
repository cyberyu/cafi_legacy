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
  'SwampDragonServices',
  'flash',
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
    }).when('/projects/:id/risks', {
      controller: 'RiskCtrl',
      templateUrl: '/static/partials/_risk.html'
    }).when('/projects/:id/relations', {
      controller: 'RelationCtrl',
      templateUrl: '/static/partials/_relation.html'
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
          if(response.status==401) {
            $rootScope.needLogin = true;
            $location.path('/');
            //$rootScope.$apply();
            return $q.reject(response);
          }
        }
    };
}]);

cafiApp.config(function ($httpProvider) {
    $httpProvider.interceptors.push('myHttpInterceptor');
});