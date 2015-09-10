'use strict';


var cafiApp = angular.module('cafiApp', ['elasticsearch', 'ngSanitize', 'ui.bootstrap', 'nya.bootstrap.select']);

cafiApp.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

cafiApp.constant('PikadayConfig', {});


