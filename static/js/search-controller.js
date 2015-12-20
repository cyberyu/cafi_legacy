/**
 * Created by yangm on 10/6/15.
 */

projectControllers.controller('GoogleSearchCtrl', function($scope,$rootScope,uiGmapGoogleMapApi, $routeParams,
                                                           $http, $uibModal, Upload, popupService, $cookies, $dragon,
                                                           Project, Search, Gdoc,GeoSearch, Company, Risk,
                                                           PredefinedSearch, RiskItem){

  $scope.user = $cookies.get('user');
  $scope.onlyMine = false;
  $scope.onlyRelevant = true;

  $scope.currentProject = {};
  $scope.currentProject.id = $routeParams.id;
  $scope.riskitems = RiskItem.query();
  $scope.predefinedCompanies = Company.query();
  $scope.predefinedRisks = Risk.query();
  $scope._relevanceScore=1;
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
  $scope.sortOption=null;

  $scope.counter = 0;
  $scope.filterOptions = ["rank", "predicted_score", "-predicted_score"];
  $scope.dataSources = ["Google", "USA Spending", "DataMyne"];
  $scope.currentSource = $scope.dataSources[0];

  //------------------- real time notification ----------------//
  $scope.channel = 'project_' + $scope.currentProject.id + '_search';
  $scope.searchStatus = {};

  $dragon.onReady(function() {
    $dragon.subscribe('search_task', $scope.channel, {project: $scope.currentProject.id}).then(function (response) {
    });
  });

  $dragon.onChannelMessage(function(channels, message) {
    if (indexOf.call(channels, $scope.channel) > -1) {
      $scope.$apply(function() {
        $scope.searchStatus = message.data;
      });
    }
  });
  //-------------------------------------------//

  $scope.selectDataSource = function(src){
    $scope.currentSource = src;
  };

  $scope.openModal = function(data) {
    $rootScope.$emit('openModal', data);
  };

  $scope.relevanceCheck='';
  $scope.showBar= 1;

  /*$scope.labeledCount = function(search){
    $scope.labelCount=0;
    Gdoc.query({"search": search.id, "relevance":'y'}).$promise.then(function (data) {
      $scope.labelCount += data.count;
      Gdoc.query({"search": search.id, "relevance":'n'}).$promise.then(function (data) {
        $scope.labelCount += data.count;
      });
    });
  };*/

  $scope.getGdocs = function(search, page, option) {
    Gdoc.query({"search": search.id, "page": page, "ordering":$scope.sortOption, "relevance":$scope.relevanceCheck}).$promise.then(function (data) {
      $scope.displaySearchDocs = data.results;
      $scope.gdocPager.total = data.count;
      $scope.gdocPager.currentPage = page;
      /*if($scope.showBar === 1){
        $scope.totalResult = $scope.gdocPager.total;
        $scope.labeledCount(search);
        $scope.showBar=0;
      }*/
    });
  };

  $scope.filterRelevance = function(option){
    $scope.relevanceCheck = option;
    $scope.getGdocs($scope.displaySearch, $scope.gdocPager.currentPage)
  };

  $scope.sortBy = function(method){
    if(method=='relevance'){
      $scope.sortOption = !$scope.sortOption || $scope.sortOption[10] != '-' ? 'relevance,-predicted_score': 'relevance,predicted_score'; // I just want sorting by predicted scores, for the relevance we have dropdown
    } else {
      $scope.sortOption = !$scope.sortOption || $scope.sortOption[0] != '-' ? '-rank': 'rank';
    }
    //console.log($scope.sortOption);
    $scope.getGdocs($scope.displaySearch, $scope.gdocPager.currentPage)
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

  $scope.pageRefresh = function(search, page){

    $scope.getGdocs(search, page);
    //$scope.labeledCount(search);
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
      $scope.totalResult = data.count;
      //$scope.labeledCount(search);
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

  $scope.updateRelevance = function (gdoc, relevance, search) {
    Gdoc.update({'id': gdoc.id, 'relevance': relevance}).$promise.then(function(data){
            $scope.relevance = data.relevance;
            console.log("gdoc id :"+ gdoc.id + "->" + $scope.relevance);
            $scope.showBar=0;
            $scope.getGdocs($scope.displaySearch, $scope.gdocPager.currentPage);
    });
    gdoc.relevance = relevance;
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
  $scope.$on('newPage', function(event, data) { $scope.displaySearchDocs=data; });
  $scope.$on('newRel', function(event, data) { $scope.getGdocs($scope.displaySearch, $scope.gdocPager.currentPage); });

  $scope.isCollapsed = true;
  $scope.listSearches(1);
  //$scope.getReviewLater(1);
  //$scope.getGdocs($scope.displaySearch, 1);
  $scope.majorRisks = Risk.query({'type':1});
  $scope.subRisks = Risk.query({'type':2});
});


