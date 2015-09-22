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
    $scope.displayMode = "edit";
    $scope.currentSearch = null;
    $scope.newSearches = [];
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
    $scope.textsToShow = [];
    $scope.showText = function(gdoc){
        if ($scope.textsToShow.indexOf(gdoc.id) >= 0)
            $scope.textsToShow.splice($scope.textsToShow.indexOf(gdoc.id), 1);
        else
            $scope.textsToShow.push(gdoc.id);
    };
    $scope.deleteGdoc = function (gdoc) {
        gdoc.$delete().then(function () {
            $scope.gdocs.splice($scope.gdocs.indexOf(gdoc), 1);
        });
    };
    $scope.listSearches();
    $scope.availableSearchNames = [{name:"Business relationships", string:'("joint venture" | "jv" | "mou" | "memorandum of understanding" | "strategic alliance" | "teaming agreement" |  "strategic partner*" | "partner" | "supplier" | "provider" | "agreement" | "contract" | "component" | "subcontract*" | "receive" | "win*")'},
        {name:"Supplier relationships", string:'("provider" | "supply" | "supplier" | "vendor" | "contract" | "fund" | "donate" | "commit" | "engineer")'}]
    $scope.companyNames = ["IBM", "Google", "Microsoft"]
    $scope.addCompany = function (newCompany) {
        if ($scope.companyNames.indexOf(newCompany) < 0) {
            $scope.companyNames.push(newCompany);
        }
    };

    $scope.generateSearches= function () {
        for(var i = 0; i < $scope.selectedSearchNames.length; i++){
            for(var j = 0; j < $scope.selectedCompanyNames.length; j++){
                var oneSearch = {};
                oneSearch.use = false;
                oneSearch.searchName = $scope.selectedSearchNames[i].name;
                oneSearch.companyName = $scope.selectedCompanyNames[j];
                oneSearch.string = $scope.selectedSearchNames[i].string + "=" + $scope.selectedCompanyNames[j];
                oneSearch.project = $scope.currentProject.id;
                $scope.newSearches.push(oneSearch);
                $scope.displayMode = "list";
            }
        }
    };

    $scope.cancelGenearateSearch = function () {
        $scope.listSearches();
        $scope.newSearches =[];
        $scope.displayMode = "edit";
    };
    $scope.batchSearch = function (newSearches) {
        var asyncLoop = function(o){
            var i=-1;

            var loop = function(){
                i++;
                if(i==o.length){o.callback(); return;}
                o.functionToLoop(loop, i);
            }
            loop();//init
        }
        asyncLoop({
            length : newSearches.length,
            functionToLoop : function(loop, i){
                var oneSearch = {};
                oneSearch.project = $scope.currentProject.id;
                oneSearch.string = newSearches[i].string;
                loop();
                new Search(oneSearch).$save().then(function() {
                });
            },
            callback : function(){
                $scope.boolGdocs = true;
                $scope.gdocs = Gdoc.query();
            }
        });

        //for(var i=0; i< newSearches.length; i++){
        //    if(newSearches[i].use){
        //        var oneSearch = {};
        //        oneSearch.project = $scope.currentProject.id;
        //        oneSearch.string = newSearches[i].string;
        //        new Search(oneSearch).$save().then(function() {
        //        });
        //        setTimeout(function(){}, 3000);
        //    }
        //}
    };
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
