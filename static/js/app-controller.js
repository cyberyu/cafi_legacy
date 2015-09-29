angular.module('projectControllers', []).controller('ProjectListCtrl', function ($scope,uiGmapGoogleMapApi,$timeout, $window, $location, $routeParams, popupService, Project) {


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
}).controller('ProjectBoardCtrl', function($scope,uiGmapGoogleMapApi, $routeParams, $http,$timeout,$interval, popupService, Project, Search, Gdoc,GeoSearch,GeoSearchResult){
    $scope.mapData = {};


    uiGmapGoogleMapApi.then(function(maps) {
        $scope.mapData.map = {center: {latitude: 40.1451, longitude: -99.6680 }, zoom: 4 };
        $scope.mapData.markers = [];

    });

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
    $scope.addresses=[];
    $scope.currentAddress = {};
    $scope.uploadAddressBool = false;
    $scope.searchedStrings = [];
    $scope.searchedGeoStrings = [];
    $scope.geoResults = [];
    $scope.counter = 0;
    $scope.csv = {
        content: null,
        header: true,
        headerVisible: false,
        separator: ',',
        separatorVisible: false,
        result: null,
        encoding: 'ISO-8859-1',
        encodingVisible: false
    };
    $scope.gsearchOptions = {};
    $scope.availableSearchNames = [
        {name:"Business relationships", string:'("joint venture" | "jv" | "mou" | "memorandum of understanding" | "strategic alliance" | "teaming agreement" |  "strategic partner*" | "partner" | "supplier" | "provider" | "agreement" | "contract" | "component" | "subcontract*" | "receive" | "win*")'},
        {name:"Supplier relationships", string:'("provider" | "supply" | "supplier" | "vendor" | "contract" | "fund" | "donate" | "commit" | "engineer")'},
        {name:"General Aerospace Components", string:'("antenna" | "convertere" | "control" | "telemetry" | "tank" | "link" | "COTS"  | "radar" | "Aft" | "data link")'},
        {name:"Conflict Minerals by name", string:'("tin" | "Cassiterite" | "Tantalum" | "Coltan" | "Columbite-Tantalite" | "Niobium" | "Tungsten"  | "Wolframite" | "Gold")'},
        {name:"Labor Disputes", string:'(strike | "labor dispute"  | violation | lawsuit | "safety violation" | employee | compliant | fine | court | arrest*)'},
        {name:"Bankruptcy", string:'("chapter 7" | "chapter 11" | "chapter 13"  | bankruptcy | debt | court |  filing | bailout)'},
        {name:"Legal Issues", string:'(lawsuit* | court* | violation | illegal | regulation* | defendant | plaitiff | failure | "cyber-attack" | espionage | suspect* | penalty | fine | ruling)'},
        {name:"Executive due deligence", string:'(arrest* | illegal | court | lawsuit | accused | alleged* | suspected | crime | jail | prison | foreign | conference | abroad | education)'},
        {name:"Business Partnerships", string:'(partnership* | "JV" | "joint venture" | "MoU" | "memorandum of understanding" | supply* | supplier | contract | agreement)'},
        {name:"General risks", string:'(crime | sabotage | protest | strike | attack | default | bankrupt | illegal | criminal | lawsuit | espionage | failure)'}];
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
        for(var i = 0; i < $scope.gsearchOptions.selectedSearchNames.length; i++){
            for(var j = 0; j < $scope.gsearchOptions.selectedCompanyNames.length; j++){
                for(var k = 0; k <$scope.gsearchOptions.selectedCompanyNames[j].variations.length; k++){
                    var oneSearch = {};
                    oneSearch.use = true;
                    oneSearch.searchName = $scope.gsearchOptions.selectedSearchNames[i].name;
                    oneSearch.companyName = $scope.gsearchOptions.selectedCompanyNames[j].variations[k];
                    oneSearch.string = $scope.gsearchOptions.selectedSearchNames[i].string + '&"' + oneSearch.companyName+'"';
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
            $scope.companyNames[$scope.companyNames.indexOf($scope.gsearchOptions.selectedCompanyNames[0])].variations.pop(selected[i]);
        }
    };
    $scope.saveEditVariation = function(newVariation){
        $scope.companyNames[$scope.companyNames.indexOf($scope.gsearchOptions.selectedCompanyNames[0])].
            variations.push(newVariation.name);
        $scope.editVariationBool = false;
        $scope.newVariation = {};
    };
    $scope.calculateProgress = function(searchedStrings, newSearches){
        var toSearches = [];
        for(var i=0; i< newSearches.length; i++){
            if(newSearches[i].use){
                toSearches.push(newSearches[i]);
            }
        }
        var result = 0;
        if(toSearches.length>0){
            result = searchedStrings.length/toSearches.length;
        }
        return result
    };
    $scope.editOrCreateAddress = function (address) {
        $scope.currentAddress =
            address ? angular.copy(address) : {};
        $scope.addAddressBool = true;
    };
    $scope.cancelAddressEdit = function () {
        $scope.currentAddress = {};
        $scope.addAddressBool = false;
    };
    $scope.saveAddressEdit = function (newAddress) {
        if (angular.isDefined(newAddress.id)) {
            $scope.updateAddress(newAddress);
        } else {
            $scope.createAddress(newAddress);
        }
    };
    $scope.createAddress = function (newAddress) {
        //new Project(project).$save().then(function(newProject) {
        //    $scope.projects.push(newProject);
        //    $scope.displayMode = "list";
        //});
        newAddress.id = $scope.addresses.length+1;
        $scope.addresses.push(newAddress);
        $scope.addAddressBool = false;
    };
    $scope.updateAddress = function (newAddress) {
        //project.$update(function(){
        //    for (var i = 0; i < $scope.projects.length; i++) {
        //        if ($scope.projects[i].id == project.id) {
        //            $scope.projects[i] = project;
        //            break;
        //        } }
        //    $scope.displayMode = "list";
        //});
        for (var i = 0; i < $scope.addresses.length; i++) {
            if ($scope.addresses[i].id == newAddress.id) {
                $scope.addresses[i] = newAddress;
                break;
            } }
        $scope.addAddressBool = false;
    };
    $scope.deleteAddress = function (address) {
        //if (popupService.showPopup('Really delete this project?')) {
        //    project.$delete().then(function () {
        //        $scope.projects.splice($scope.projects.indexOf(project), 1);
        //    });
        //}
        $scope.addresses.splice($scope.addresses.indexOf(address), 1);

    };
    $scope.uploadAddress = function(){
        String.prototype.replaceAll = function(str1, str2, ignore)
        {
            return this.replace(new RegExp(str1.replace(/([\,\!\\\^\$\{\}\[\]\(\)\.\*\+\?\|\<\>\-\&])/g, function(c){return "\\" + c;}), "g"+(ignore?"i":"")), str2);
        };
        for(var i = 0;i < $scope.csv.result.length; i ++){
            var newAdd = {id: $scope.addresses.length+1,
                name: $scope.csv.result[i]['"name"'].replaceAll('"',''),
                address: $scope.csv.result[i]['"address"'].replaceAll('"','')
            }
            $scope.addresses.push(newAdd);
        }
    };

    $scope.batchGeoSearch = function () {
        var timeInt = 100;
        $scope.progressBool = true;
        var toSearches = [];
        for(var i=0;i < $scope.addresses.length; i++){
            toSearches.push($scope.addresses[i]);
        }
        $interval(function() {
            if (toSearches.length >0) {
                var item = toSearches.pop();
                var oneSearch = {
                    project: $scope.currentProject.id,
                    string: item.address};
                $http.post('/api/geosearch',oneSearch)
                    .success(function(data) {
                        $scope.searchedGeoStrings.push(data);
                        $scope.addresses[$scope.addresses.indexOf(item)].id = data.id;
                    });
            } else {
                $interval.cancel();
            }
        }, timeInt);
        $interval(function() {
            if ($scope.counter < $scope.addresses.length) {
                $scope.counter++
            } else {
                $interval.cancel();
            }
        }, 10*timeInt);
        $timeout(function(){
            $scope.geoResultsBool = true;
            $scope.geoResults = GeoSearchResult.query(function(){
                for(var j=0; j < $scope.addresses.length; j++){
                    for(var i=0; i < $scope.geoResults.length; i++){
                        if($scope.geoResults[i].search == $scope.addresses[j].id){
                            $scope.addresses[j].lat = $scope.geoResults[i].lat;
                            $scope.addresses[j].lng = $scope.geoResults[i].lng;
                        }
                    }
                }
                for(var j=0; j < $scope.addresses.length; j++){
                    var newMarker = {
                        id: $scope.addresses[j].id,
                        latitude: $scope.addresses[j].lat,
                        longitude: $scope.addresses[j].lng
                    };
                    $scope.mapData.markers.push(newMarker);
                }
            });

            $scope.counter = 0;
        }, 10*timeInt*toSearches.length);
    };

    $scope.calculateProgressAddress = function(addresses){
        var result = 0;
        if(addresses.length>0){
            result = $scope.counter/addresses.length;
        }
        return result
    };
    $scope.centerMap = function(address){
        $scope.mapData.map = {center: {latitude: address.lat, longitude: address.lng }, zoom: 12 };
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
