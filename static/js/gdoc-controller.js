projectControllers.controller('gDocCtrl', function ($scope, $modalInstance,$uibModal, currentDoc, $http, $q, Gdoc, Risk) {

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

  $scope.selectedBuyerCompany = null;
  $scope.selectedSupplierCompany = null;
  $scope.newRisk = {};

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
        object_id: $scope.currentDoc.id,
        fromCompany: $scope.newRisk.selectedFromCompany.id,
        toCompany: $scope.selectedToCompany,
        risk: $scope.newRisk.majorRisk.id,
        subrisk: $scope.newRisk.subRisk.id,
        risk_type: 1,
        content_type: "searchresult"
      };

      $http.post('/api/risk_items', oneLabel)
        .success(function(data) {
          $scope.currentDoc.risks.push(data);
          $scope.newRisk = {};
        });
    });
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
