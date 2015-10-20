projectControllers.controller('advancedSearchCtrl', function ($scope, $http, $interval, $timeout, $modalInstance,
                                                              $routeParams, Upload, Search, Company, Risk) {
  $scope.project_id = $routeParams.id;

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

  $scope.companyNames = Company.query({"project__id": $scope.project_id});

  $scope.ok = function () {
    $modalInstance.close();
    $scope.listSearches();
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
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
    var toSearches = [];
    for(var i=0; i< newSearches.length; i++){
      if(newSearches[i].use){
        toSearches.push(newSearches[i]);
      }
    }
    $http.post('/api/gsearch/batch', toSearches);

    $scope.msg = toSearches.length + ' search strings were successfully submitted to the server.';
    $scope.msg_class = "alert-success";
    $scope.showSearchListBool = false;
  };

  $scope.addCompany = function () {
    $scope.editCompanyBool = true;
    $scope.editVariationBool = false;
  };

  $scope.saveEditCompany = function (newCompany) {
    if(newCompany.name) {
      if (newCompany.to_variations) newCompany.variations = newCompany.to_variations.split(';');
      console.log(newCompany.variations);

      if (newCompany.id) {
        var obj = Company.update(newCompany);
      } else {
        newCompany.project = $scope.project_id;
        var obj = Company.save(newCompany);
        $scope.companyNames.push(obj);
      }
    }
    $scope.editCompanyBool = false;
    $scope.newCompany = {};
  };

  $scope.deleteCompanies = function(selected){
    for(var i =0; i <selected.length; i++){
      if(selected[i].id) Company.delete({"companyId": selected[i].id});
      $scope.companyNames.pop(selected[i]);
    }
  };

  $scope.editCompany = function(selected){
    if(selected && selected.length==1){
      $scope.editCompanyBool = true;
      $scope.editVariationBool = false;
      $scope.newCompany = selected[0];
      $scope.newCompany.to_variations = selected[0].variations.join(';');
    } else {
      $scope.msg = "Please select one item";
      $scope.msg_class = "alert-danger";
    }
  };

  $scope.cancelEditCompany = function(){
    $scope.newCompany = {};
    $scope.editCompanyBool = false;
  };

  $scope.addSearchName = function(){
    $scope.editSearchNameBool = true;
  };

  $scope.saveEditSearchName = function(newSearchName){
    if(newSearchName.name && newSearchName.searchString) {
      if(newSearchName.id) {
        var newSearch = Risk.update(newSearchName);
      } else {
        var newSearch = Risk.save(newSearchName);
        $scope.availableSearchNames.push(newSearch);
      }
    }
    $scope.editSearchNameBool = false;
    $scope.newSearchName = {};
  };

  $scope.deleteSearchNames = function(selected){
    for(var i =0; i <selected.length; i++){
      if(selected[i].id) Risk.delete({"riskId": selected[i].id});
      $scope.availableSearchNames.pop(selected[i]);
    }
  };

  $scope.editSearchName = function(selected){
    if (selected && selected.length == 1){
      $scope.editSearchNameBool = true;
      $scope.newSearchName = selected[0];
    } else {
      $scope.msg = "Please select one item";
      $scope.msg_class = "alert-danger";
    }
  };

  $scope.cancelEditSearchName = function(){
    $scope.newSearchName = {};
    $scope.editSearchNameBool = false;
  };

  $scope.addVariation = function(){
    $scope.editCompanyBool = false;
    $scope.editVariationBool = true;
  };

  $scope.deleteVariations = function(selected){
    for(var i =0; i <selected.length; i++){
      $scope.gsearchOptions.selectedCompanyNames[0].variations.pop(selected[i]);
    }
    $scope.saveEditCompany($scope.gsearchOptions.selectedCompanyNames[0]);
  };

  $scope.cancelEditVariation = function(){
    $scope.newVariation = {};
    $scope.editVariationBool = false;
  };

  $scope.saveEditVariation = function(newVariation){
    $scope.gsearchOptions.selectedCompanyNames[0].variations.push(newVariation.name);
    $scope.saveEditCompany($scope.gsearchOptions.selectedCompanyNames[0]);
    $scope.editVariationBool = false;
    $scope.newVariation = {};
  };

  $scope.uploadFiles = function(file, errFiles) {
    $scope.f = file;
    file.progress = 0;
    $scope.errFile = errFiles && errFiles[0];
    if (file) {
      file.upload = Upload.upload({
        url: '/api/companies/'+$scope.project_id+'/upload',
        data: {file: file}
      });

      file.upload.then(function (response) {
        $timeout(function () {
          $scope.companyNames = response.data;
        });
      }, function (response) {
        if (response.status > 0)
          $scope.errorMsg = response.status + ': ' + response.data;
      }, function (evt) {
        file.progress = Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
      });
    }
  };
});
