/**
 * Created by pengfeiz on 10/20/15. Modified by tanmoypatra 11/18/15
 */

projectControllers.controller('mapCtrl', function($scope, uiGmapGoogleMapApi, uiGmapIsReady, GeoSearch){
  $scope.map = {center: {latitude: 40.1451, longitude: -99.6680}, zoom: 4};
  $scope.options = {scrollwheel: false};

  $scope.markers = [];
  uiGmapIsReady.promise().then(function(){
    var options = {"project": $scope.project_id, "size":1000};
    GeoSearch.query(options).$promise.then(function (data) {
      $scope.allAddresses = data.results;
      angular.forEach($scope.allAddresses, function(address){
        marker = {
          id: address.id,
          coords: { "latitude": address.lat, "longitude": address.lng},
          info: address.name + ': ' + address.address
        };
        $scope.markers.push(marker);
      });
    });
  });

  $scope.deleteAllMarkers= function(){
    $scope.markers=[];
  };

  $scope.deleteMarker =function(address){
    for (var i = $scope.markers.length - 1; i >= 0; i--) {
      if ($scope.markers[i].id === address.id) {
        $scope.markers.splice(i, 1);
      }
    }
  };

  $scope.locateOnMap = function(address){

    var flag=0;
    for (var i = $scope.markers.length - 1; i >= 0; i--) {
      if ($scope.markers[i].id === address.id) {
        flag=1;
      }
    }
    if(flag===0){
      marker = {
          id: address.id,
          coords: { "latitude": address.lat, "longitude": address.lng},
          info: address.name + ': ' + address.address
        };
      $scope.markers.push(marker);
      console.log("Marker Created");
    }

    $scope.markers.map(function(marker){
      marker.icon = 'http://maps.google.com/mapfiles/ms/icons/red-dot.png';
    });
    angular.forEach($scope.markers, function(marker){
      if (marker.id == address.id){
        marker.icon = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png';
      }
    });
    $scope.map.center.latitude = address.lat;
    $scope.map.center.longitude = address.lng;
    $scope.map.zoom = 4;
    $scope.title = address.name;
  }
});