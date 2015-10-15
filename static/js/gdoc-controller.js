projectControllers.controller('gDocCtrl', function ($scope, $modalInstance, currentDoc) {

  $scope.currentDoc = currentDoc;
  console.log($scope.currentPage);

  $scope.ok = function () {
    $modalInstance.close($scope.selected.item);
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
