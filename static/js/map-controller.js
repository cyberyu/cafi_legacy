/**
 * Created by pengfeiz on 10/20/15. Modified by tanmoypatra 11/18/15
 */

projectControllers.controller('mapCtrl', function($scope, uiGmapGoogleMapApi, uiGmapIsReady){

    uiGmapGoogleMapApi.then(function (maps) {
        //$scope.googlemap = {};
        $scope.map = {
            center: {
                latitude: 40.1451,
                longitude: -99.6680
            },
            zoom: 4,
            pan: 1,
            options: $scope.mapOptions,
            control: {},
            events: {
                tilesloaded: function (maps, eventName, args) {},
                dragend: function (maps, eventName, args) {},
                zoom_changed: function (maps, eventName, args) {}
            }
        };
    });
    $scope.options = {scrollwheel: false};
    $scope.marker = {
        title: 'Address',
        address: "",
        coords: {
            latitude: 40.1451,
            longitude: -99.6680
        },
        visible: false,
        id: 0
    };
    $scope.windowOptions = {
        show:false
    };

    $scope.windowOptions1 = {
        visible: false
    };

    $scope.onClick1 = function () {
        $scope.windowOptions.visible = !$scope.windowOptions.visible;
    };

    $scope.onClick = function (data) {
        console.log(data);
        $scope.windowOptions.show = !$scope.windowOptions.show;
        console.log('$scope.windowOptions.show: ', $scope.windowOptions.show);
        console.log('Office Name ' + data);
        //alert('This is a ' + data);
    };
    $scope.info = "Bug! Info issue"; // Trying to set in onclick, but it doesn't reflect

    $scope.closeClick1 = function () {
        $scope.windowOptions.visible = false;
    };

    $scope.closeClick = function () {
        $scope.windowOptions.show = false;
    };

    uiGmapIsReady.promise() // if no value is put in promise() it defaults to promise(1)
        .then(function (instances) {
            console.log(instances[0].map); // get the current map
        })
        .then(function () {
            $scope.markers = [];
            for (var i = 0; i < $scope.addresses.length; i++) {
                $scope.markers.push({
                    id: $scope.markers.length,
                    coords: {
                        latitude: $scope.addresses[i].lat,
                        longitude: $scope.addresses[i].lng
                    },
                    data: $scope.addresses[i].name
                });
            }
            $scope.addMarkerClickFunction($scope.markers);
        });

    $scope.addMarkerClickFunction = function (markersArray) {
        angular.forEach(markersArray, function (value, key) {
            console.log(value);
            value.onClick = function () {
                $scope.info = value.data;
                $scope.onClick(value.data);
                $scope.MapOptions.markers.selected = value;
            };
        });
    };
    $scope.MapOptions = {
        minZoom: 3,
        zoomControl: false,
        draggable: true,
        navigationControl: false,
        mapTypeControl: false,
        scaleControl: false,
        streetViewControl: false,
        disableDoubleClickZoom: false,
        keyboardShortcuts: true,
        markers: {
            selected: {}
        },
        styles: [{
            featureType: "poi",
            elementType: "labels",
            stylers: [{
                visibility: "off"
            }]
        }, {
            featureType: "transit",
            elementType: "all",
            stylers: [{
                visibility: "off"
            }]
        }],
    };


    $scope.locateOnMap = function(address){
        console.log("Individual Marker");
        $scope.marker.coords.latitude = address.lat;
        $scope.marker.coords.longitude = address.lng;
        $scope.map.center.latitude = address.lat;
        $scope.map.center.longitude = address.lng;
        $scope.map.zoom = 4;
        $scope.marker.title = address.name;
        $scope.marker.address = address.address;

    };

});