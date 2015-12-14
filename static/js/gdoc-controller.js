projectControllers.controller('gDocCtrl', function ($scope, $modalInstance,$uibModal, currentDoc, $http, Gdoc, Risk) {

  $scope.currentDoc = currentDoc;
  $scope.tags = [];

  $scope.shouldShow = function (item) {
    return item!=$scope.majorRisk;
  };

  $scope.shouldShow1= function (item) {
    return item!=$scope.majorRisk && item!=$scope.secondaryRisk;
  };

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
  //Code for trial of pool
  $scope.displayMode = "list";
  $scope.currentRelation = null;

  $scope.listRelations = function () {
    $scope.relations = Relation.query();
  };

  $scope.deleteRelation = function (relation) {
    if (popupService.showPopup('Really delete this Supply Chain?')) {
      Relation.$delete().then(function () {
        $scope.relations.splice($scope.relations.indexOf(relation), 1);
      });
    }
  };

  $scope.editOrCreateRelation = function (relation) {
    $scope.currentRelation =
      relation ? angular.copy(relation) : {};
    $scope.displayMode = "edit";
  };

  $scope.createRelation = function (relation) {
    new Relation(relation).$save().then(function(newRelation) {
      $scope.relations.push(newRelation);
      $scope.displayMode = "list";
    });
  };

  $scope.saveEdit = function (newRelation) {
    if (angular.isDefined(newRelation.id)) {
      $scope.updateRelation(newRelation);
    } else {
      $scope.createRelation(newRelation);
    }
  };

  $scope.updateRelation = function (relation) {
    relation.$update(function(){
      for (var i = 0; i < $scope.relations.length; i++) {
        if ($scope.relations[i].id == relation.id) {
          $scope.relations[i] = relation;
          break;
        } }
      $scope.displayMode = "list";
    });
  };

  $scope.cancelEdit = function () {
    $scope.currentRelation = {};
    $scope.displayMode = "list";
  };

  //$scope.listRelations(); //have to creation a supply chain backend relation

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

  function createTag1(companyId) {
    //$scope.tags = [];
    $scope.tags.push( "Company Created: " + companyId);
  }


  $scope.selectedBuyerCompany = null;
  $scope.selectedSupplierCompany = null;
  $scope.majorRisk = null;
  $scope.secondaryRisk = null;
  $scope.tertiaryRisk = null;


  $scope.labelRiskSubmit = function () {
    //WIP
    console.log("Major,Secondary ..Risk API is to be created");
  };

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
  $scope.companySubmit = function () {
    for (var i = 0; i < $scope.predefinedCompanies.length; i++) {
      if ($scope.predefinedCompanies[i].name == $scope.selectedFromCompany1) {
        var selectedFromCompanyID = $scope.predefinedCompanies[i].id;
        break;
      }
    }
    var oneCompany = {
      name:$scope.selectedFromCompany1,
      variations: [$scope.selectedFromCompany1],
      project:$scope.currentProject.id
    };

    if($scope.noResults){
      $http.post('/api/companies', oneCompany)
        .success(function(postedCompany){
          createTag1(postedCompany.name);
          $scope.predefinedCompanies.push(postedCompany);
          console.log($scope.predefinedCompanies);
      });
    } else {
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

  $scope.addRisks = function(w){
    console.log(w.id);
    Risk.get({riskId: w.id}).$promise.then(function(data){
      $scope.searchString = data.searchString;
      console.log($scope.searchString);
    });
    //WIP
    /*if (!$scope.currentDoc.risk) $scope.currentDoc.risk = [];
    $scope.currentDoc.risk.push(w);*/
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
      $scope.tags = [];
    });
    $scope.selectedBuyerCompany = null;
    $scope.selectedSupplierCompany = null;
  };

  $scope.ok = function () {
    $modalInstance.close($scope.selected.item);
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };

  $scope.major_risk = ["Capacity Constraints", "Financial Distress", "Labor Unrest", "IP Loss", "Conflict Mineral Sourcing", "Import/Export Violations", "Counterfeit/Non-MIL SPEC Parts",
  "Legal", "Counterfeit","Conflict Minerals", "Financial", "Capacity", "Specialty Metals"];
});
