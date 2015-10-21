/**
 * Created by pengfeiz on 10/20/15.
 */
projectControllers.controller('mapCtrl', function($scope){

    $scope.map = {center: {latitude: 40.1451, longitude: -99.6680}, zoom: 4};
    $scope.options = {scrollwheel: false};
    $scope.marker = {
        coords: {
            latitude: 40.1451,
            longitude: -99.6680
        },
        show: false,
        id: 0
    };

    $scope.windowOptions = {
        visible: false
    };

    $scope.onClick = function () {
        $scope.windowOptions.visible = !$scope.windowOptions.visible;
    };

    $scope.closeClick = function () {
        $scope.windowOptions.visible = false;
    };

    $scope.title = 'Address';

    $scope.locateOnMap = function(address){
        $scope.marker.coords.latitude = address.lat;
        $scope.marker.coords.longitude = address.lng;
        $scope.map.center.latitude = address.lat;
        $scope.map.center.longitude = address.lng;
        $scope.map.zoom = 12;
        $scope.title = address.name;

    }

});