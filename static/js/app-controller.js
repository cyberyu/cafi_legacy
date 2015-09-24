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
}).controller('ProjectBoardCtrl', function($scope, $routeParams, $http,$timeout,$interval, popupService, Project, Search, Gdoc){
    $scope.currentProject = Project.get({id:$routeParams.id});
    $scope.currentSearch = null;
    $scope.newSearches = [];
    $scope.progressBool = false;
    $scope.editSearchNameBool = false;
    $scope.newSearchName = {};
    $scope.editCompanyBool = false;
    $scope.newCompany = {};
    $scope.editVariationBool = false;
    $scope.newVariation = {};
    $scope.showSearchListBool = false;
    $scope.availableSearchNames = [{name:"Business relationships", string:'("joint venture" | "jv" | "mou" | "memorandum of understanding" | "strategic alliance" | "teaming agreement" |  "strategic partner*" | "partner" | "supplier" | "provider" | "agreement" | "contract" | "component" | "subcontract*" | "receive" | "win*")'},
        {name:"Supplier relationships", string:'("provider" | "supply" | "supplier" | "vendor" | "contract" | "fund" | "donate" | "commit" | "engineer")'}];
    $scope.companyNames = [{name:"IBM", variations:["IBM Global Business Service", "IBM Research", "IBM Global Technology Service", "IBM India"]},
        {name:"Microsoft", variations:["Microsoft Research", "Microsoft India"]}];
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

    $scope.generateSearches= function () {
        $scope.newSearches =[];
        for(var i = 0; i < $scope.selectedSearchNames.length; i++){
            for(var j = 0; j < $scope.selectedCompanyNames.length; j++){
                for(var k = 0; k <$scope.selectedCompanyNames[j].variations.length; k++){
                    var oneSearch = {};
                    oneSearch.use = true;
                    oneSearch.searchName = $scope.selectedSearchNames[i].name;
                    oneSearch.companyName = $scope.selectedCompanyNames[j].variations[k];
                    oneSearch.string = $scope.selectedSearchNames[i].string + '&"' + oneSearch.companyName+'"';
                    oneSearch.project = $scope.currentProject.id;
                    $scope.newSearches.push(oneSearch);
                }
            }
        }
        $scope.showSearchListBool = true;

    };
    $scope.cancelGenearateSearch = function () {
        $scope.listSearches();
        $scope.newSearches =[];
        $scope.showSearchListBool = false;

    };
    $scope.searchedStrings = [];
    $scope.batchSearch = function (newSearches) {
        var timeInt = 2000;
        $scope.progressBool = true;
        var toSearches = [];
        for(var i=0; i< newSearches.length; i++){
            if(newSearches[i].use){
                toSearches.push(newSearches[i]);
            }
        }
        $interval(function() {
            if (toSearches.length >0) {
                var item = toSearches.pop();
                var oneSearch = {
                project: $scope.currentProject.id,
                string: item.string};
                $http.post('/api/gsearch',oneSearch)
                    .success(function(data) {
                    });
                $scope.searchedStrings.push(oneSearch);
            } else {
                $interval.cancel();
            }
        }, timeInt);
        $timeout(function(){
            $scope.boolGdocs = true;
            $scope.gdocs = Gdoc.query();
        }, timeInt*toSearches.length);
    };
    $scope.addCompany = function () {
        $scope.editCompanyBool = true;
    };
    $scope.saveEditCompany = function (newCompany) {
        $scope.companyNames.push(newCompany);
        $scope.editCompanyBool = false;
        $scope.newCompany = {};
    };
    $scope.deleteCompanies = function(selected){
        for(var i =0; i <selected.length; i++){
            $scope.companyNames.pop(selected[i]);
        }
    };
    $scope.addSearchName = function(){
        $scope.editSearchNameBool = true;
    };
    $scope.saveEditSearchName = function(newSearchName){
        $scope.availableSearchNames.push(newSearchName);
        $scope.editSearchNameBool = false;
        $scope.newSearchName = {};
    };
    $scope.deleteSearchNames = function(selected){
        for(var i =0; i <selected.length; i++){
            $scope.availableSearchNames.pop(selected[i]);
        }
    };
    $scope.addVariation = function(){
        $scope.editVariationBool = true;
    };
    $scope.deleteVariations = function(selected){
        for(var i =0; i <selected.length; i++){
            $scope.companyNames[$scope.companyNames.indexOf($scope.selectedCompanyNames[0])].variations.pop(selected[i]);
        }
    };
    $scope.saveEditVariation = function(newVariation){
        $scope.companyNames[$scope.companyNames.indexOf($scope.selectedCompanyNames[0])].
            variations.push(newVariation.name);
        $scope.editVariationBool = false;
        $scope.newVariation = {};
    };
    $scope.listSearches();
    $scope.gdocs = Gdoc.query();
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
