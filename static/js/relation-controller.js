projectControllers.controller('RelationCtrl', function($scope,$rootScope,uiGmapGoogleMapApi, $routeParams, $q,
                                                           $http, $uibModal, Upload, popupService, $cookies,
                                                           Project, Search, Gdoc,GeoSearch, Company,
                                                           Relation, RiskItem) {
  $scope.currentProject = {};
  $scope.currentProject.id = $routeParams.id;

  $scope.Relations = Relation.query({"project": $scope.currentProject.id});
  $scope.predefinedCompanies = Company.query();

  $scope.sortBy = function(method){
    if(method=='buyer'){
      $scope.sortOption = !$scope.sortOption || $scope.sortOption[0] != '-' ? '-buyer__name': 'buyer__name';
    } else {
      $scope.sortOption = !$scope.sortOption || $scope.sortOption[0] != '-' ? '-supplier__name': 'supplier__name';
    }
    var option = {'ordering':$scope.sortOption,'buyer':$scope.filterBuyer,'supplier':$scope.filterSupplier, 'items':$scope.filterItems};
    $scope.getRelation(option);
  };

  $scope.findBy = function(method,query){
    if(method=='buyer'){
      $scope.filterBuyer = query;

    }else if(method=='supplier'){
      $scope.filterSupplier = query;
    }else{
      $scope.filterItems = query;
    }
    option = {'ordering':$scope.sortOption, 'buyer':$scope.filterBuyer,'supplier':$scope.filterSupplier, 'items':$scope.filterItems};
    //console.log(option);
    $scope.getRelation(option);
  };

  $scope.getRelation = function(option) {
    var options = {"project": $scope.currentProject.id};
    angular.extend(options, option);
    //$scope.Relations = Relation.query(options);
    Relation.query(options).$promise.then(function (data) {
      $scope.Relations = data;
    });
  };

  $scope.createCompany = function(name){
    var oneCompany = {
      name: name,
      variations: [name],
      project:$scope.currentProject.id
    };

    return Company.save(oneCompany);
  };

  $scope.createRelation = function () {
    var one, two;
    if($scope.noBuyerResults) {
      one = $scope.createCompany($scope.newRelation.buyer).$promise.then(function(postedCompany){
        $scope.predefinedCompanies.push(postedCompany);
        $scope.newRelation.buyer = postedCompany;
      });
    }

    if($scope.noSupplierResults) {
      two = $scope.createCompany($scope.newRelation.supplier).$promise.then(function(postedCompany){
        $scope.predefinedCompanies.push(postedCompany);
        $scope.newRelation.supplier = postedCompany;
      });
    }

    $q.all([one, two]).then(function() {
      var relation = {
        //evidence: $scope.currentDoc.id,
        exEvidence: $scope.exEvidence,
        buyer: $scope.newRelation.buyer.id,
        supplier: $scope.newRelation.supplier.id,
        items: $scope.newRelation.items,
        project: $scope.currentProject.id
      };

      Relation.save(relation).$promise.then(function (newRelation) {
        $scope.Relations.push(newRelation);
        $scope.newRelation = {};
      });
    });
  };
});
