/**
 * Created by yangm on 10/6/15.
 */

projectControllers.controller('GoogleSearchCtrl', function($scope,$rootScope,uiGmapGoogleMapApi, $routeParams,
                                                           $http, $uibModal, Upload, popupService, $cookies,
                                                           Project, Search, Gdoc,GeoSearch, Company, Risk, RiskItem){

  $scope.user = $cookies.get('user');
  $scope.onlyMine = false;
  $scope.onlyRelevant = true;

  $scope.currentProject = {};
  $scope.currentProject.id = $routeParams.id;
  $scope.riskitems = RiskItem.query();
  $scope.predefinedCompanies = Company.query();
  $scope.predefinedRisks = Risk.query();

  $scope.searchPager = {};
  $scope.searchPager.currentPage = 1;
  $scope.searchPager.total = null;

  $scope.gdocPager = {};
  $scope.gdocPager.currentPage = 1;
  $scope.gdocPager.total = null;

  $scope.currentSearch = null;
  $scope.search = {};
  $scope.gsearchOptions = {};

  $scope.searches = [];

  $scope.counter = 0;
  $scope.filterOptions = ["General", "Relevance", "Irrelevance"];
  $scope.dataSources = ["Google", "USA Spending", "DataMyne"];
  $scope.currentSource = $scope.dataSources[0];
  $scope.selectDataSource = function(src){
    $scope.currentSource = src;
  };

  $scope.openModal = function(data) {
    $rootScope.$emit('openModal', data);
  };

  $scope.getGdocs = function(search, page) {
    Gdoc.query({"search": search.id, "page": page}).$promise.then(function (data) {
      $scope.displaySearchDocs = data.results;
      $scope.gdocPager.total = data.count;
      $scope.gdocPager.currentPage = page;
    });
  };

  $scope.getReviewLater = function(page){
    Gdoc.query({search__project: $scope.currentProject.id, review_later: 'True', page: page}).$promise.then(function(data){
      $scope.displaySearchDocs = data.results;
      $scope.gdocPager.total = data.count;
      $scope.gdocPager.currentPage = page;
      $scope.displaySearch = null;
      $scope.reviewLaterActive = true;
    })
  };

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

  $scope.activeSearch = function(){
    var actSearch = {
      project: $scope.currentProject.id
    };
    $http.post('/api/Relevancefilter', actSearch)
      .success(function(data) {
        console.log(data);
      });
    console.log(actSearch);
  };

  $scope.moreSearch = function(n){
    $http.post('/api/gsearch/'+$scope.displaySearch.id+'/demand_page');
    console.log('get one more')
  };

  $scope.setDisplaySearch = function(search){
    Gdoc.get({search: search.id}).$promise.then(function(data){
      $scope.displaySearchDocs = data.results;
      $scope.gdocPager.total = data.count;
      $scope.gdocPager.currentPage = 1;
      $scope.displaySearch = search;
      $scope.reviewLaterActive = false;
    });
  };

  $scope.toggleOnlyMine = function(){
    $scope.onlyMine = !$scope.onlyMine;
    $scope.listSearches(1);
  };

  $scope.listSearches = function (page) {
    var options = {"project": $scope.currentProject.id, "page": page};
    if ($scope.onlyMine) { options["user"] = $scope.user; }
    if ($scope.onlyRelevant) {options['is_relevant'] = 'True'; }

    Search.query(options).$promise.then(function(data){
      $scope.searches = data.results;
      $scope.displaySearch = $scope.searches[0];
      $scope.getGdocs($scope.displaySearch, 1);

      $scope.searchPager.total = data.count;
      $scope.searchPager.currentPage = page;
    });
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

  $scope.toggleSearchJunk = function(search){
    if (search.isRelevant) {
      Search.update({id: search.id, is_relevant: false}).$promise.then(function(search){
        $scope.searches.splice($scope.searches.indexOf(search),1);
      });
    } else {
      Search.update({id: search.id, is_relevant: true}).$promise.then(function(search){
        console.log('mark as relevant')
      });
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

  $scope.updateRelevance = function (gdoc, relevance) {
    //console.log(gdoc);
    Gdoc.update({'id': gdoc.id, 'relevance': relevance}).$promise.then(function(data){
            $scope.relevance = data.relevance;
            console.log("gdoc id :"+ gdoc.id + "->" + $scope.relevance);
          });
    /*x = (Gdoc.get({"gdocId": gdoc.id}).$promise.then(function(data){
            $scope.relevance = data.relevance;
            console.log($scope.relevance);
          }));*/
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
      scope: $scope
      //windowClass: 'gen-search-modal'
    });

    $scope.modalInstance.result.then(function(){
      console.log('---')
    }, function(){
      console.log('dismissed');
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
  $scope.listSearches(1);
  //$scope.getReviewLater(1);
  //$scope.getGdocs($scope.displaySearch, 1);

});


