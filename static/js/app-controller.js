angular.module('projectControllers', []).controller('ProjectListCtrl', function ($scope, $window, $location, $routeParams, popupService, Project) {
    $scope.projects = Project.query();
    $scope.orderProp = 'created_at';
    $scope.addBool = false;
    $scope.editBool = false;
    $scope.deleteProject = function (project) {
        if (popupService.showPopup('Really delete this?')) {
            project.$delete(function () {
                $window.location.href = '';
            });
        }
    }
    $scope.setAddBoolTrue = function () {
        $scope.addBool = true;
        $scope.editBool = false;
    }
    $scope.setEditBoolTrue = function (project) {
        $scope.projectToEdit = Project.get({ projectId: project.id}, function() {
            $scope.editBool = true;
            $scope.addBool = false;
        });
    }
    $scope.setAddBoolFalse= function () {
        $scope.addBool = false;
    }
    $scope.setEditBoolFalse= function () {
        $scope.editBool = false;
    }
    $scope.project = new Project();
    $scope.addProject = function () {
        $scope.project.$save(function () {
            $scope.projects = Project.query();
            $scope.addBool = false;
        });
    }
    $scope.updateProject=function(){
        $scope.projectToEdit.$update(function(){
            $scope.projects = Project.query();
            $scope.editBool = false;
        });
    };

})


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
    }

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
