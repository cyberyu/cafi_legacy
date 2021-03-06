projectControllers.controller('GeoSearchCtrl', function($scope,$rootScope,uiGmapGoogleMapApi,
                                                           $routeParams, $http,$timeout, $uibModal,
                                                           $interval, Upload, popupService, Project,
                                                           Search, Gdoc,GeoSearch,$window, $dragon){

  $scope.project_id = $routeParams.id;
  $scope.currentProject = {id: $scope.project_id};

  $scope.channel = 'project_'+$scope.project_id+'_geo';
  $scope.taskStatus = {numberGood: 0, numberBad: 0};

  $dragon.onReady(function() {
    $dragon.subscribe('geo_task', $scope.channel, {project: $scope.project_id}).then(function (response) {
    });
  });

  $dragon.onChannelMessage(function(channels, message) {
    if (indexOf.call(channels, $scope.channel) > -1) {
      $scope.$apply(function() {
        if (message.data.good) {
          $scope.taskStatus.numberGood += 1;
        } else {
          $scope.taskStatus.numberBad += 1;
        }
        $scope.taskStatus.numberProcessed = $scope.taskStatus.numberGood + $scope.taskStatus.numberBad;
      });
    }
  });

  $scope.findEntity = function(name){
    $scope.filterName = name;
    option = {'page':$scope.currentPage,'name':$scope.filterName,'address':$scope.filterAddress};
    //console.log(option);
    $scope.getAddresses(option);
  };

  $scope.findAddress = function(address){
    $scope.filterAddress = address;
    option = {'page':$scope.currentPage,'address':$scope.filterAddress,'name':$scope.filterName};
    //console.log(option);
    $scope.getAddresses(option);

  };

  $scope.sortEntity = function(method) {
    $scope.sortOption = !$scope.sortOption || $scope.sortOption[0] != '-' ? '-name': 'name';
    option = {'page':$scope.currentPage,'ordering':$scope.sortOption,'name':$scope.filterName,'address':$scope.filterAddress};
    $scope.getAddresses(option);
  };

  $scope.sortAddress = function(method) {
    $scope.sortOption = !$scope.sortOption || $scope.sortOption[0] != '-' ? '-address': 'address';
    option = {'page':$scope.currentPage,'ordering':$scope.sortOption,'name':$scope.filterName,'address':$scope.filterAddress};
    $scope.getAddresses(option);
  };

  $scope.uploadFiles = function(file, errFiles) {
    $scope.f = file;
    file.progress = 0;
    $scope.errFile = errFiles && errFiles[0];
    if (file) {
      file.upload = Upload.upload({
        url: '/api/Upload',
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
    var deleteAll = $window.confirm('This would delete all Geo.');
    if (deleteAll) {
      for (var i = 0; i < $scope.addresses.length; i++) {
        console.log($scope.addresses[i].name);
        if ($scope.addresses[i].id) {
          $http.delete('/api/geosearch/' + $scope.addresses[i].id);
        }
      }
      $scope.addAddressBool = false;
      $scope.geoRefresh();

    }

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
      $scope.taskStatus.numberSubmitted = response.data.count > 0 ? response.data.count : 0 ;
      if ($scope.taskStatus.numberSubmitted>0) {
        $scope.hasPendingJob = true;
      }
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
