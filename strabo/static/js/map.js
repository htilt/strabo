
function set_feature_click(all_layers_group){
    var all_layers = all_layers_group.getLayers();
    all_layers.forEach(function(layer){
        layer.on({
            click: function(e){ip_clicked(e.target.feature.properties.db_id)}
        });
    });
}

$(document).ready(function(){
    var map = make_map('map');
    add_tile_to(map);

    var all_layers_group = L.geoJson(features);

    flickity_init();
    map.addControl( new L.Control.Compass() ); //compass feature will not work on devices that do not have a compass

    set_styles(all_layers_group);
    place_overlays_on(all_layers_group,map);
    bind_popups(all_layers_group);

    set_feature_click(all_layers_group);
    set_geolocation(map);

});

function set_geolocation(map){

    // Current solution to keep geoLocation only
    // relevant in the campus/canyon area is to set
    // map bounds. Also vital to leaflet-locatecontrol.

    // NOTE: GETS REAL WEIRD AND JUMPY IN SAFARI
    // However, works fine in Google Chrome

    var northWest = L.latLng(45.48469, -122.63892);
    var southEast = L.latLng(45.47897, -122.62268);
    var bounds = L.latLngBounds(northWest, southEast);

    map.setMaxBounds(bounds);

    L.control.locate({
        locateOptions:{enableHighAccuracy:true},
        icon: "fa fa-crosshairs",
        iconElementTag:"a",
        onLocationOutsideMapBounds:function(control){
            // When outside of bounds, centers on the Canyon the button is clicked
            map.setView([straboconfig["LAT_SETTING"], straboconfig["LONG_SETTING"]], straboconfig["INITIAL_ZOOM"]);
            control.stop();
        },
        keepCurrentZoomLevel:true,
        circleStyle: {
            color: '#136AEC',
            fillColor: '#136AEC',
            fillOpacity: 0.15,
            weight: 4,
            opacity: 0.5
        },
        markerStyle: {
            color: '#ffffff',
            fillColor: '#2A93EE',
            fillOpacity: 0.7,
            weight: 2,
            opacity: 0.9,
            radius: 10
        },
        strings: {
            popup: "You are within {distance} {unit} of this point"
        },
    }).addTo(map)
      .start(); // Starts looking for your location when page loads, instead of waiting for button to be clicked
}
