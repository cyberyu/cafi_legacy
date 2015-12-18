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
