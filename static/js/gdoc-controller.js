projectControllers.controller('gDocCtrl', function ($scope, $modalInstance,$uibModal, currentDoc, $http, $q,
                                                    Gdoc, Risk, Relation, Company) {

  $scope.currentDoc = currentDoc;
  $scope.tags = [];

  for (var i = 0; i < $scope.displayedGdocs.length; i++) {
    if ($scope.displayedGdocs[i].id == $scope.currentDoc.id) {
      $scope.currentID = ($scope.gdocPager.currentPage - 1)*20 + (i + 1);
      break;
    }
  }
  if (i < $scope.displayedGdocs.length -1){
    $scope.nextID = $scope.displayedGdocs[i+1].id;
  }else{
    $scope.nextID = null;
  }

  //$scope.relations = Relation.query({evidence: currentDoc.id});

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
        evidence: $scope.currentDoc.id,
        buyer: $scope.newRelation.buyer.id,
        supplier: $scope.newRelation.supplier.id,
        items: $scope.newRelation.items,
        project: $scope.currentProject.id
      };

      Relation.save(relation).$promise.then(function (newRelation) {
        $scope.currentDoc.relations.push(newRelation);
        $scope.newRelation = {};
      });
    });
  };

  $scope.saveEditRelation = function () {
    if (angular.isDefined($scope.newRelation.id)) {
      $scope.updateRelation($scope.newRelation);
    } else {
      $scope.createRelation();
    }
  };

  $scope.updateRelation = function (relation) {
    relation.$update(function(){
      for (var i = 0; i < $scope.relations.length; i++) {
        if ($scope.relations[i].id == relation.id) {
          $scope.relations[i] = relation;
          break;
        } }
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


  $scope.updateRelevance = function (newDoc,relevance) {
    Gdoc.update({'id': newDoc.id, 'relevance': relevance}).$promise.then(function(data){
            $scope.relevance = data.relevance;
            console.log("gdocId:"+ newDoc.id + "->" + $scope.relevance);
          });
    newDoc.relevance = relevance;
  };

  $scope.toggleSave4later = function(newDoc){
    Gdoc.update({id: newDoc.id, review_later: !newDoc.reviewLater}).$promise.then(function(data){
      $scope.currentDoc = data;
    });
  };

  //$scope.addKeywords = function(w){
  //  if (!$scope.currentDoc.ner) $scope.currentDoc.ner = [];
  //  $scope.currentDoc.ner.push(w);
  //};
  //
  //$scope.addRisks = function(w){
  //  console.log(w.id);
  //  Risk.get({riskId: w.id}).$promise.then(function(data){
  //    $scope.searchString = data.searchString;
  //    console.log($scope.searchString);
  //  });
  //  //WIP
  //  /*if (!$scope.currentDoc.risk) $scope.currentDoc.risk = [];
  //  $scope.currentDoc.risk.push(w);*/
  //};


  $scope.openNextGdoc = function (n) {

    var flag = 0;
    for (var i = 0; i < $scope.displayedGdocs.length; i++) {
      if ($scope.displayedGdocs[i].id == $scope.currentDoc.id) {
        $scope.currentID = ($scope.gdocPager.currentPage - 1)*20 + (i + 1);
        break;
      }
    }
    if ((i < $scope.displayedGdocs.length-1 && !(i === 0 && n === -1)) || (i === $scope.displayedGdocs.length-1 && n === -1)){
      $scope.nextID = $scope.displayedGdocs[i+n].id;
    }else{
      flag = 1;
      Gdoc.query({"search": $scope.displaySearch.id, "page": $scope.gdocPager.currentPage + n, "ordering":$scope.sortOption}).$promise.then(function (data) {
        $scope.displaySearchDocs = data.results;
        $scope.gdocPager.total = data.count;
        $scope.gdocPager.currentPage = $scope.gdocPager.currentPage + n;
        if(n === -1){
          $scope.nextID = $scope.displaySearchDocs[$scope.displaySearchDocs.length - 1].id;
        }else{
          $scope.nextID = $scope.displaySearchDocs[0].id;
        }

        $scope.displayedGdocs = $scope.displaySearchDocs;
        Gdoc.get({"gdocId": $scope.nextID}).$promise.then(function(data){
          $scope.currentDoc = data;
          $scope.tags = [];
        });
        $scope.currentID += n;
        $scope.selectedBuyerCompany = null;
        $scope.selectedSupplierCompany = null;
      });
    }
    if(flag === 0) {
      Gdoc.get({"gdocId": $scope.nextID}).$promise.then(function (data) {
        $scope.currentDoc = data;
        $scope.tags = [];
      });
      $scope.selectedBuyerCompany = null;
      $scope.selectedSupplierCompany = null;
      $scope.currentID += n;
    }
  };

  $scope.ok = function () {
    $modalInstance.close($scope.selected.item);
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };

  //$scope.major_risk = ["Capacity Constraints", "Financial Distress", "Labor Unrest", "IP Loss", "Conflict Mineral Sourcing", "Import/Export Violations", "Counterfeit/Non-MIL SPEC Parts",
  //"Legal", "Counterfeit","Conflict Minerals", "Financial", "Capacity", "Specialty Metals"];
});
