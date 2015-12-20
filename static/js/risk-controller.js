projectControllers.controller('RiskCtrl', function($scope,$rootScope, $routeParams, $q,
                                                           $http, $uibModal, popupService, $cookies,
                                                           Project, Search, Gdoc, GeoSearch, Company, Risk,
                                                           PredefinedSearch, RiskItem) {
  $scope.currentProject = {};
  $scope.currentProject.id = $routeParams.id;

  $scope.majorRisks = Risk.query({'type':1});
  $scope.predefinedCompanies = Company.query();

  $scope.Risks = RiskItem.query({"project": $scope.currentProject.id});
  $scope.subRisks = Risk.query({'type':2});

  $scope.sortBy = function(method){
    if(method=='company') {
      $scope.sortOption = !$scope.sortOption || $scope.sortOption[0] != '-' ? '-from_company' : 'from_company';
    }
    var option = {'ordering':$scope.sortOption,'from_company':$scope.filterCompany,'risk':$scope.filterRisk, 'subrisk':$scope.filterSubRisk};
    $scope.getRisk(option);
  };

  $scope.findBy = function(method,query){
    if(method=='company'){
      $scope.filterCompany = query;

    }else if(method=='risk'){
      $scope.filterRisk = query;
    }else{
      $scope.filterSubRisk = query;
    }
    var option = {'ordering':$scope.sortOption,'from_company':$scope.filterCompany,'risk':$scope.filterRisk, 'subrisk':$scope.filterSubRisk};
    //console.log(option);
    $scope.getRisk(option);
  };

  $scope.getRisk = function(option) {
    var options = {"project": $scope.currentProject.id};
    angular.extend(options, option);
    RiskItem.query(options).$promise.then(function (data) {
      $scope.Risks = data;
    });
  };

  $scope.labelRiskSubmit = function () {
    var one, two;

    if($scope.noResults){
      var oneCompany = {
        name: $scope.newRisk.selectedFromCompany,
        variations: [$scope.newRisk.selectedFromCompany],
        project:$scope.currentProject.id
      };

      var one = $http.post('/api/companies', oneCompany)
        .success(function(postedCompany){
          $scope.newRisk.selectedFromCompany = postedCompany;
          $scope.predefinedCompanies.push(postedCompany);
        });
    }

    if($scope.noSubRiskResults){
      var oneSubRisk = {
        name: $scope.newRisk.subRisk,
        type: 2,
        parent: $scope.newRisk.majorRisk.id
      };

      var two = $http.post('/api/risks', oneSubRisk)
        .success(function(data){
          $scope.newRisk.subRisk = data;
          $scope.subRisks.push(data);
        });
    }

    $q.all([one, two]).then(function(){
      var oneLabel = {
        project: $scope.currentProject.id,
        fromCompany: $scope.newRisk.selectedFromCompany.id,
        toCompany: $scope.selectedToCompany,
        risk: $scope.newRisk.majorRisk.id,
        subrisk: $scope.newRisk.subRisk.id,
        //risk_type: 1,
        exEvidence: $scope.exEvidence
      };

      $http.post('/api/risk_items', oneLabel)
        .success(function(data) {
          $scope.Risks.push(data);
          $scope.newRisk = {};
        });
    });
  };
});
