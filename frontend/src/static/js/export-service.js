
var esExportLocation = window.location.origin + '/_export';

SearchApp.service('exportService', function ($http) {
	return {
		exportData: function( reqBody ){
			return $http.post( esExportLocation, reqBody ).then(function(result) {
           				return result;
					});
		}
	};
});

