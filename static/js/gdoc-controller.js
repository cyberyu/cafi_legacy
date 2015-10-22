projectControllers.controller('gDocCtrl', function ($scope, $modalInstance,$uibModal, currentDoc, $http, Gdoc) {

  $scope.currentDoc = currentDoc;
  $scope.currentDoc.createdAt = Date($scope.currentDoc.createdAt);
  $scope.tags = [];
  for (var i = 0; i < $scope.riskitems.length; i++) {
    if ($scope.riskitems[i].objectId == $scope.currentDoc.id) {
      $scope.tags.push( $scope.riskitems[i].risk + " Risk from " +  $scope.riskitems[i].fromCompany + " to " + $scope.riskitems[i].toCompany)
    }
  }
  for (var i = 0; i < $scope.displayedGdocs.length; i++) {
    if ($scope.displayedGdocs[i].id == $scope.currentDoc.id) {
      break;
    }
  }
  if (i < $scope.displayedGdocs.length -1){
    $scope.nextID = $scope.displayedGdocs[i+1].id;
  }else{
    $scope.nextID = null;
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

  $scope.addKeywords = function(w){
    if (!$scope.currentDoc.ner) $scope.currentDoc.ner = [];
    $scope.currentDoc.ner.push(w);
  };

  $scope.openNextGdoc = function () {
    for (var i = 0; i < $scope.displayedGdocs.length; i++) {
      if ($scope.displayedGdocs[i].id == $scope.currentDoc.id) {
        break;
      }
    }
    if (i < $scope.displayedGdocs.length -1){
      $scope.nextID = $scope.displayedGdocs[i+1].id;
    }else{
      $scope.nextID = null;
    }
    Gdoc.get({"gdocId": $scope.nextID}).$promise.then(function(data){
      $scope.currentDoc = data;
      $scope.currentDoc.createdAt = Date($scope.currentDoc.createdAt);
      $scope.tags = [];
    });
  };

  $scope.ok = function () {
    $modalInstance.close($scope.selected.item);
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
