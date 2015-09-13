
cafiApp.factory('Project', ['$resource', function($resource) {
    return $resource('/projects/:projectId.json', null,
    {
      'query': {method:'GET', params:{projectId:''}, isArray:true}
    });
}]);


