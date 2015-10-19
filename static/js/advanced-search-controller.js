projectControllers.controller('advancedSearchCtrl', function ($scope, $http, $interval, $timeout, $modalInstance, Search, Gdoc) {
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

  $http.get('/api/risks').then(function(response){
    $scope.availableSearchNames = response.data;
  });

  $http.get('/api/companies').then(function(response){
    $scope.companyNames = response.data;
  });

  $scope.ok = function () {
    $modalInstance.close($scope.selected.item);
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
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

});
