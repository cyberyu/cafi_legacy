angular.module('projectControllers', []).controller('ProjectListCtrl', function ($scope, $window, $location, $routeParams, popupService, Project) {
    $scope.displayMode = "list";
    $scope.currentProject = null;
    $scope.listProjects = function () {
        $scope.projects = Project.query();
    };
    $scope.deleteProject = function (project) {
        if (popupService.showPopup('Really delete this project?')) {
            project.$delete().then(function () {
                $scope.projects.splice($scope.projects.indexOf(project), 1);
            });
        }
    };
    $scope.createProject = function (project) {
        new Project(project).$save().then(function(newProject) {
            $scope.projects.push(newProject);
            $scope.displayMode = "list";
        });
    };
    $scope.saveEdit = function (newProject) {
        if (angular.isDefined(newProject.id)) {
            $scope.updateProject(newProject);
        } else {
            $scope.createProject(newProject);
        }
    };
    $scope.editOrCreateProject = function (project) {
        $scope.currentProject =
            project ? angular.copy(project) : {};
        $scope.displayMode = "edit";
    };
    $scope.updateProject = function (project) {
            project.$update(function(){
                for (var i = 0; i < $scope.projects.length; i++) {
                    if ($scope.projects[i].id == project.id) {
                        $scope.projects[i] = project;
                        break;
                    } }
                $scope.displayMode = "list";
            });
    };
    $scope.cancelEdit = function () {
        $scope.currentProject = {};
        $scope.displayMode = "list";
    };
    $scope.listProjects();
}).controller('ProjectBoardCtrl', function($scope, $routeParams, popupService, Project, Search, Gdoc){
    $scope.currentProject = Project.get({id:$routeParams.id});
    $scope.displayMode = "list";
    $scope.currentSearch = null;
    $scope.listSearches = function () {
        $scope.searches = Search.query();
    };
    $scope.deleteSearch = function (search) {
        if (popupService.showPopup('Really delete this Search?')) {
            search.$delete().then(function () {
                $scope.searches.splice($scope.searches.indexOf(search), 1);
            });
        }
    };
    $scope.createSearch= function (search) {
        search.project = $scope.currentProject.id;
        new Search(search).$save().then(function(newSearch) {
            $scope.searches.push(newSearch);
            $scope.displayMode = "list";
        });
    };
    $scope.saveEdit = function (newSearch) {
        if (angular.isDefined(newSearch.id)) {
            $scope.updateSearch(newSearch);
        } else {
            $scope.createSearch(newSearch);
        }
    };
    $scope.editOrCreateSearch = function (search) {
        $scope.currentSearch =
            search ? angular.copy(search) : {};
        $scope.displayMode = "edit";
    };
    $scope.updateSearch = function (search) {
        search.$update(function(){
            for (var i = 0; i < $scope.projects.length; i++) {
                if ($scope.projects[i].id == search.id) {
                    $scope.projects[i] = search;
                    break;
                } }
            $scope.displayMode = "list";
        });
    };
    $scope.cancelEdit = function () {
        $scope.currentProject = {};
        $scope.displayMode = "list";
    };
    $scope.showGdocs = function(){
        $scope.boolGdocs = !$scope.boolGdocs;
        $scope.gdocs = Gdoc.query();
    };
    $scope.boolGdocs = false;
    $scope.listSearches();
});

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
