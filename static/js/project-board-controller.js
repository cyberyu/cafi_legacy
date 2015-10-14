/**
 * Created by yangm on 10/6/15.
 */

projectControllers.controller('ProjectBoardCtrl', function($scope, $routeParams, Project) {

    $scope.currentProject = {};
    $scope.currentProject.id = $routeParams.id;

});

