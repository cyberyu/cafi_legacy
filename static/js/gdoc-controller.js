projectControllers.controller('gDocCtrl', function ($scope, $modalInstance, currentDoc, $http) {

  $scope.currentDoc = currentDoc;
  $scope.currentDoc.createdAt = Date($scope.currentDoc.createdAt);

  $scope.tags = [];
  for (var i = 0; i < $scope.riskitems.length; i++) {
    if ($scope.riskitems[i].objectId == $scope.currentDoc.id) {
      $scope.tags.push( $scope.riskitems[i].risk + " Risk from " +  $scope.riskitems[i].fromCompany + " to " + $scope.riskitems[i].toCompany)
    }
  }


  $scope.labelSubmit = function () {
    var oneLabel = {
      project: $scope.currentProject.id,
      object_id: $scope.currentDoc.id,
      fromCompany: $scope.selectedFromCompany,
      toCompany: $scope.selectedToCompany,
      risk:$scope.selectedRisk,
      content_type: "searchresult"
    };
    $http.post('/api/risk_items', oneLabel)
        .success(function(data) {
          $scope.riskitems.push(data);
          $scope.tags = [];
          for (var i = 0; i < $scope.riskitems.length; i++) {
            if ($scope.riskitems[i].objectId == $scope.currentDoc.id) {
              $scope.tags.push( $scope.riskitems[i].risk + " Risk from " +  $scope.riskitems[i].fromCompany + " to " + $scope.riskitems[i].toCompany)
            }
          }
        });
  };


  $scope.ok = function () {
    $modalInstance.close($scope.selected.item);
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
