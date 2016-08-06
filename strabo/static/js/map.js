//sets the popup feature when you click a spot on the map
function set_map_click(map){
    // Display latlng info for any place on the map when clicked
    function onMapClick(e) {
       L.popup()
        .setLatLng(e.latlng)
        .setContent(e.latlng.toString())
        .openOn(map);
    }
    // Trigger onMapClick function whenever map is clicked
    map.on('click', onMapClick);
}
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

    flickety_init();

    var all_layers_group = L.geoJson(features);
    set_styles(all_layers_group);
    place_overlays_on(all_layers_group,map);
    bind_popups(all_layers_group);
    set_feature_click(all_layers_group);

    set_map_click(map);

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
            //when outside of bounds, it centers over canyon when button is clicked.
            map.setView([straboconfig["LAT_SETTING"], straboconfig["LONG_SETTING"]], straboconfig["INITIAL_ZOOM"]);
            control.stop();
        },
        keepCurrentZoomLevel:true
    }).addTo(map)
      .start();//starts looking for your location when page loads, instead of waiting for button to be clicked
}
