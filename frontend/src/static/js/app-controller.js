
cafiApp.controller('projectListCtrl', ['$scope', '$routeParams', 'Project',
  function($scope, $routeParams, Project) {
    $scope.projects = Project.query();
    $scope.orderProp = 'created_at';
  }
]);
