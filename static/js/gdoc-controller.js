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


  function createTag(companyId) {
    var oneLabel = {
      project: $scope.currentProject.id,
      object_id: $scope.currentDoc.id,
      fromCompany: companyId,
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
  }

  $scope.labelSubmit = function () {
    for (var i = 0; i < $scope.predefinedCompanies.length; i++) {
      if ($scope.predefinedCompanies[i].name == $scope.selectedFromCompany) {
        var selectedFromCompanyID = $scope.predefinedCompanies[i].id;
        break;
      }
    }
    var oneCompany = {
      name:$scope.selectedFromCompany,
      variations: [$scope.selectedFromCompany],
      project:$scope.currentProject.id
    };

    if($scope.noResults){
      $http.post('/api/companies', oneCompany)
        .success(function(postedCompany){
          createTag(postedCompany.id);
          $scope.predefinedCompanies.push(postedCompany);
          console.log($scope.predefinedCompanies);
      });
    } else {
        createTag(selectedFromCompanyID)
    }
  };

  $scope.updateRelevance = function (newDoc) {
    Gdoc.update({'id': newDoc.id, 'relevance': newDoc.relevance})
  };

  $scope.toggleSave4later = function(newDoc){
    Gdoc.update({id: newDoc.id, review_later: !newDoc.reviewLater}).$promise.then(function(data){
      $scope.currentDoc = data;
    });
  };

  $scope.addKeywords = function(w){
    if (!$scope.currentDoc.ner) $scope.currentDoc.ner = [];
    $scope.currentDoc.ner.push(w);
  };

  $scope.openNextGdoc = function (n) {
    for (var i = 0; i < $scope.displayedGdocs.length; i++) {
      if ($scope.displayedGdocs[i].id == $scope.currentDoc.id) {
        break;
      }
    }
    if (i < $scope.displayedGdocs.length-1){
      $scope.nextID = $scope.displayedGdocs[i+n].id;
    }else{
      $scope.getGdocs($scope.displaySearch, $scope.gdocPager.currentPage+1);
      $scope.nextID = $scope.displaySearchDocs[0];
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
