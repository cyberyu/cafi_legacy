projectControllers.controller('GeoSearchCtrl', function($scope,$rootScope,uiGmapGoogleMapApi,
                                                           $routeParams, $http,$timeout, $uibModal,
                                                           $interval, Upload, popupService, Project,
                                                           Search, Gdoc,GeoSearch){

  $scope.project_id = $routeParams.id;
  $scope.currentProject = {};
  $scope.currentProject.id = $routeParams.id;

  console.log($scope.project_id)

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
          $scope.addresses = response.data.items.concat($scope.addresses);
        });
      }, function (response) {
        if (response.status > 0)
          $scope.errorMsg = response.status + ': ' + response.data;
      }, function (evt) {
        file.progress = Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
      });
    }
  };

  $scope.getAddresses = function(option) {
    var options = {"project": $scope.project_id};
    angular.extend(options, option);
    GeoSearch.query(options).$promise.then(function (data) {
      $scope.addresses = data.results;
      $scope.total = data.count;
      if (option.page) { $scope.currentPage = option.page; }
    });
  };

  $scope.getAddresses({page:1});

  $scope.currentAddress = {};
  $scope.uploadAddressBool = false;
  $scope.geoResults = [];

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
    //newAddress.id = $scope.addresses.length+1;
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
  $scope.deleteAllGeoSearch = function(){
    for (var i = 0; i < $scope.addresses.length; i++) {
      console.log($scope.addresses[i].name);
      if($scope.addresses[i].id) {
        $http.delete('/api/geosearch/' + $scope.addresses[i].id);
      }
    }
    $scope.addAddressBool = false;

  };

  $scope.getAddressClass = function(address){
    if (address.lat && address.lng){
      return ""
    } else if (address.status=='bad') {
      return "danger"
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

  $scope.submitGeoSearch = function(){
    $http.post('/api/geosearch/'+$scope.project_id+'/batch', $scope.addresses).then(function(response){
      $scope.submitDisabled = true;
      $scope.numberSubmitted = response.data.count > 0 ? response.data.count : 0 ;
      console.log($scope.numberSubmitted);
    });
  };

  $scope.geoRefresh = function(page){
    $scope.getAddresses($scope.currentPage);
  };

  $scope.geoDownload = function(){
    $http.get('/api/geosearch/'+$scope.project_id+'/download').then(function(response){

    });
  };

  $scope.openGeoEdit = function (size, address) {
    $scope.currentAddress =
      address ? angular.copy(address) : {};
    $scope.addAddressBool = true;

    var modalInstance = $uibModal.open({
      animation: false,
      templateUrl: 'geoModal.html',
      controller: 'geoModalCtrl',
      size: size,
      scope: $scope
    });

    modalInstance.result.then(function (selectedItem) {
      $scope.selected = selectedItem;
    }, function () {
      console.log('Modal dismissed at: ' + new Date());
    });
  };

});

projectControllers.controller('geoModalCtrl', function ($scope, $modalInstance){

  $scope.ok = function () {
    $modalInstance.close();
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
