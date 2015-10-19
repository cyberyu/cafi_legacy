/**
 * Created by yangm on 10/6/15.
 */

projectControllers.controller('GoogleSearchCtrl', function($scope,$rootScope,uiGmapGoogleMapApi, $routeParams,
                                                           $http,$timeout,$interval, $uibModal, Upload, popupService,
                                                           Project, Search, Gdoc,GeoSearch){

  //Project.get({projectId:$routeParams.id}, function(data){
  //  $scope.currentProject = data;
  //});

  $scope.currentProject = {};
  $scope.currentProject.id = $routeParams.id;



  $scope.openModal = function(data) {
    $rootScope.$emit('openModal', data);
  };


  $scope.mapData = {};
  uiGmapGoogleMapApi.then(function(maps) {
    $scope.mapData.map = {center: {latitude: 40.1451, longitude: -99.6680 }, zoom: 4 };
    $scope.mapData.markers = [];

  });


  $http.get('/api/gsearch?project='+$scope.currentProject.id).then(function(response){
    if(response.data.count > 0){
      console.log(response.data.count)
      $scope.displaySearch = response.data.results[0];
      console.log($scope.displaySearch);
      Gdoc.get({search:$scope.displaySearch.id}, 1).$promise.then(function(data){
        $scope.displaySearchDocs = data.results;
        $scope.total = data.count;
        $scope.currentPage = 1;
      });
    }
  });

  $scope.getGdocs = function(search, page) {
    Gdoc.query({"search": search.id, "page": page}).$promise.then(function (data) {
      $scope.displaySearchDocs = data.results;
      $scope.total = data.count;
      $scope.currentPage = page;
    });
  };

  $scope.currentPage = 1;
  $scope.currentSearch = null;
  $scope.search = {};
  $scope.newSearches = [];
  $scope.progressBool = false;
  $scope.editSearchNameBool = false;
  $scope.newSearchName = {};
  $scope.editCompanyBool = false;
  $scope.newCompany = {};
  $scope.editVariationBool = false;
  $scope.newVariation = {};
  $scope.showSearchListBool = false;

  $scope.searchedStrings = [];
  $scope.counter = 0;

  $scope.submitSearch = function(){
    var oneSearch = {
      project: $scope.currentProject.id,
      status: 0,
      string: $scope.search.string
    };
    $http.post('/api/gsearch', oneSearch)
      .success(function(data) {
        $scope.searches.push(data);
      });
  };

  $scope.gsearchOptions = {};

  $scope.setDisplaySearch = function(search){
    Gdoc.get({search:search.id}).$promise.then(function(data){
      $scope.displaySearchDocs = data.results;
      $scope.total = data.count;
      $scope.currentPage = 1;
      $scope.displaySearch = search;
    });
  };

  $http.get('/api/risks').then(function(response){
    $scope.availableSearchNames = response.data;
  });

  $http.get('/api/companies').then(function(response){
    $scope.companyNames = response.data;
  });

  $scope.listSearches = function () {
    $scope.searches = Search.query({"project": $scope.currentProject.id});
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
    Gdoc.delete({"gdocId": gdoc.id}).$promise.then(function(){
      $scope.displaySearchDocs.splice($scope.displaySearchDocs.indexOf(gdoc), 1);
    });
  };

  $scope.generateSearches= function () {
    $scope.newSearches =[];
    for(var j = 0; j < $scope.gsearchOptions.selectedCompanyNames.length; j++){
      for(var i = 0; i < $scope.gsearchOptions.selectedSearchNames.length; i++){
        var variations = [];
        angular.forEach($scope.gsearchOptions.selectedCompanyNames[j].variations, function(v){
          variations.push('"'+v+'"');
        });
        var companyVariations = variations.join(' | ');

        var oneSearch = {};
        oneSearch.use = true;
        oneSearch.searchName = $scope.gsearchOptions.selectedSearchNames[i].name;
        oneSearch.companyName = $scope.gsearchOptions.selectedCompanyNames[j].name;
        oneSearch.companyNameString = '"'+$scope.gsearchOptions.selectedCompanyNames[j].name + '" | ' + companyVariations;
        oneSearch.string = '(' + $scope.gsearchOptions.selectedSearchNames[i].searchString + ') & (' + oneSearch.companyNameString +')';
        oneSearch.project = $scope.currentProject.id;
        $scope.newSearches.push(oneSearch);
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

  // modal stuff
  $scope.openGdoc = function (size, doc) {
    $scope.modalInstance = $uibModal.open({
      animation: true,
      templateUrl: '/static/partials/_gdoc.html',
      controller: 'gDocCtrl',
      size: size,
      scope: $scope,
      resolve: {
        currentDoc: function(){
          $scope.currentDoc = angular.copy(doc) ;
          //$scope.currentDocRelevant = $scope.currentDoc.label;
          //$scope.currentDocTags = $scope.currentDoc.docType;
          $scope.currentDoc.createdAt = Date($scope.currentDoc.createdAt);
          return $scope.currentDoc;
        }
      }
    });

    $scope.modalInstance.result.then(function (selectedItem) {
      console.log('---')
    }, function () {
      console.log('Modal dismissed at: ' + new Date());
    });
  };


  $scope.saveEdit = function (newDoc) {
    $http.put('/api/gdocs/' + newDoc.id, newDoc).success(function(data) {
      for (var i = 0; i < $scope.displaySearchDocs.length; i++) {
        if ($scope.displaySearchDocs[i].id == newDoc.id) {
          $scope.displaySearchDocs[i] = newDoc;
          break;
        }
      }
      for (var i = 0; i < $scope.displayedGdocs.length; i++) {
        if ($scope.displayedGdocs[i].id == newDoc.id) {
          $scope.displayedGdocs[i] = newDoc;
          break;
        }
      }
      $scope.modalInstance.dismiss('cancel');
    });
  };


  //$scope.cancel = function () {
  //  $scope.modalInstance.dismiss('cancel');
  //};
  //
  //$scope.review = function(doc){
  //  alert('aa');
  //};

  $scope.isCollapsed = true;
  $scope.listSearches();
  //$scope.getGdocs($scope.displaySearch, 1);

});


