projectControllers.controller('ProjectListCtrl', function ($scope,uiGmapGoogleMapApi,$timeout, $window, $location, $routeParams, popupService, Project) {


  $scope.displayMode = "list";
  $scope.currentProject = null;
  $scope.listProjects = function () {
    $scope.projects = Project.query();
  };

  $scope.deleteProject = function (project) {
    if (popupService.showPopup('Really delete this project?')) {
      project.$delete().then(function () {
        $scope.projects.splice($scope.projects.indexOf(project), 1);
      });
    }
  };

  $scope.createProject = function (project) {
    new Project(project).$save().then(function(newProject) {
      $scope.projects.push(newProject);
      $scope.displayMode = "list";
    });
  };

  $scope.saveEdit = function (newProject) {
    if (angular.isDefined(newProject.id)) {
      $scope.updateProject(newProject);
    } else {
      $scope.createProject(newProject);
    }
  };

  $scope.editOrCreateProject = function (project) {
    $scope.currentProject =
      project ? angular.copy(project) : {};
    $scope.displayMode = "edit";
  };

  $scope.updateProject = function (project) {
    project.$update(function(){
      for (var i = 0; i < $scope.projects.length; i++) {
        if ($scope.projects[i].id == project.id) {
          $scope.projects[i] = project;
          break;
        } }
      $scope.displayMode = "list";
    });
  };

  $scope.cancelEdit = function () {
    $scope.currentProject = {};
    $scope.displayMode = "list";
  };

  $scope.listProjects();
});


