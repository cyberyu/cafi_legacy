/**
 * Created by yangm on 10/6/15.
 */

projectControllers.controller('ProjectBoardCtrl', function($scope,$rootScope,uiGmapGoogleMapApi, $routeParams, $http,$timeout,$interval, Upload, popupService, Project, Search, Gdoc,GeoSearch,GeoSearchResult){

  $scope.project_id = $routeParams.id;

  $scope.uploadFiles = function(file, errFiles) {
    $scope.f = file;
    file.progress = 0;
    $scope.errFile = errFiles && errFiles[0];
    if (file) {
      file.upload = Upload.upload({
        url: '/api/upload',
        data: {file: file}
      });

      file.upload.then(function (response) {
        $timeout(function () {
          //file.result = response.data;
          $scope.addresses = $scope.addresses.concat(response.data.items);
        });
      }, function (response) {
        if (response.status > 0)
          $scope.errorMsg = response.status + ': ' + response.data;
      }, function (evt) {
        file.progress = Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
      });
    }
  };

  $scope.openModal = function(data) {
    $rootScope.$emit('openModal', data);
  };


  $scope.mapData = {};
  uiGmapGoogleMapApi.then(function(maps) {
    $scope.mapData.map = {center: {latitude: 40.1451, longitude: -99.6680 }, zoom: 4 };
    $scope.mapData.markers = [];

  });
  $scope.currentProject = Project.get({id:$routeParams.id});

  $http.get('/api/gsearch').then(function(response){
    $scope.displaySearch = response.data.results[0];
    $scope.displaySearchDocs = Gdoc.get({search:$scope.displaySearch.id});
  });

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
  $scope.addresses=GeoSearch.query({"project__id": 1});
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
  $scope.setDisplaySearch = function(search){
    $scope.displaySearchDocs = Gdoc.get({search:search.id});
    $scope.displaySearch = search;
  };

  $http.get('/api/risks').then(function(response){
    $scope.availableSearchNames = response.data;
  });

  $http.get('/api/companies').then(function(response){
    $scope.companyNames = response.data;
  });

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
    newAddress.id = $scope.addresses.length+1;
    $scope.addresses.push(newAddress);
    $scope.addAddressBool = false;
  };
  $scope.updateAddress = function (newAddress) {
    for (var i = 0; i < $scope.addresses.length; i++) {
      if ($scope.addresses[i].id == newAddress.id) {
        $scope.addresses[i] = newAddress;
        break;
      } }
    $scope.addAddressBool = false;
  };
  $scope.deleteAddress = function (address) {
    $scope.addresses.splice($scope.addresses.indexOf(address), 1);
    if(address.id) {
      $http.delete('/api/geosearch/' + address.id);
    }
  };

  $scope.getAddressClass = function(address){
    if (address.lat && address.lng){
      return ""
    } else {
      return "warning"
    }
  };

  $scope.getLatLon = function(address){
    address.project = $scope.project_id;
    if (address.id) {
      $http.patch('/api/geosearch/'+address.id, address).then(function () {
        console.log('good');
      })
    } else {
      $http.post('/api/geosearch', address).then(function () {
        console.log('good');
      })
    }
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

  $scope.submitGeoSearch = function(){
    $http.post('/api/geosearch/'+$scope.project_id+'/batch', $scope.addresses).then(function(response){
      $scope.submitDisabled = true;
      $scope.numberSubmitted = response.data.count > 0 ? response.data.count : 0 ;
      console.log($scope.numberSubmitted);
    });
  };

  $scope.geoRefresh = function(){
    $http.get('/api/geosearch').then(function(response){
      $scope.addresses = response.data.results;
    })
  };

  $scope.geoDownload = function(){
    $http.get('/api/geosearch/'+$scope.project_id+'/download').then(function(response){

    });
  };

  $scope.centerMap = function(address){
    $scope.mapData.map = {center: {latitude: address.lat, longitude: address.lng }, zoom: 12 };
  };
  $scope.listSearches();
  $scope.gdocs = Gdoc.query();
}).controller('modal', function($scope,$rootScope){
  $scope.modalClass = 'closed';
  $rootScope.$on('openModal', function(event, data) {
    $scope.data = data;
    $scope.modalClass = 'open';
  });
});

