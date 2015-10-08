/**
 * Created by yangm on 10/6/15.
 */

cafiApp.controller('loginCtrl', function ($scope, $routeParams, $http, $location) {
  $scope.is_login = false;
  $scope.username = 'aa';

  $scope.login = function () {
    $http.post('/login/', $scope.loginForm)
      .success(function (data) {
        $scope.username = data.username;
        $scope.is_login = true;
        if ($scope.is_login) {
          $location.path('/projects');
        }
      })
  };

  $scope.me = function () {
    $http.get('/me/')
      .success(function (data) {
        $scope.is_login = data.is_login;
        $scope.username = data.username;
        if ($scope.is_login) {
          $location.path('/projects');
        }
      })
  };

  $scope.register = function () {
    $http.post('/register/', $scope.registerForm)
      .success(function (data) {
        location.reload();
      }
    )
  };

  $scope.me();
});
