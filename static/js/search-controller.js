/**
 * Created by yangm on 10/6/15.
 */

projectControllers.controller('GoogleSearchCtrl', function($scope,$rootScope,uiGmapGoogleMapApi, $routeParams,
                                                           $http, $uibModal, Upload, popupService,
                                                           Project, Search, Gdoc,GeoSearch, Company, Risk, RiskItem){

  //Project.get({projectId:$routeParams.id}, function(data){
  //  $scope.currentProject = data;
  //});

  $scope.currentProject = {};
  $scope.currentProject.id = $routeParams.id;
  $scope.riskitems = RiskItem.query();
  $scope.predefinedCompanies = Company.query();
  $scope.predefinedRisks = Risk.query();

  $scope.dataSources = ["Google", "USA Spending", "DataMyne"];
  $scope.currentSource = $scope.dataSources[0];
  $scope.selectDataSource = function(src){
    $scope.currentSource = src;
  };

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

  // modal stuff
  $scope.openGdoc = function (size, gdoc) {
    $scope.modalInstance = $uibModal.open({
      animation: true,
      templateUrl: '/static/partials/_gdoc.html',
      controller: 'gDocCtrl',
      size: size,
      scope: $scope,
      resolve: {
        currentDoc: function(){
          return Gdoc.get({"gdocId": gdoc.id}).$promise.then(function(data){
            return data;
          });
        }
      }
    });

    $scope.modalInstance.result.then(function (selectedItem) {
      console.log('---')
    }, function () {
      console.log('Modal dismissed at: ' + new Date());
    });
  };

  $scope.openGenSearch = function(size){
    $scope.modalInstance = $uibModal.open({
      animation: true,
      templateUrl: '/static/partials/_gen_search.html',
      controller: 'advancedSearchCtrl',
      size: size,
      scope: $scope,
      //windowClass: 'gen-search-modal'
    });

    $scope.modalInstance.result.then(function(){
      console.log('---')
    }, function(){
      console.log('dismissed');
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
      //$scope.modalInstance.dismiss('cancel');
    });
  };

  $scope.status = {
    isopen: false
  };

  $scope.toggled = function(open) {
    $log.log('Dropdown is now: ', open);
  };

  $scope.toggleDropdown = function($event) {
    $event.preventDefault();
    $event.stopPropagation();
    $scope.status.isopen = !$scope.status.isopen;
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


