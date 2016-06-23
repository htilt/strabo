var map;

//is called whenever a leafelet feature is clicked
function whenClicked(e) {
    ip_clicked(e.target.feature.properties.db_id);
}

//sets the popup feature when you click a spot on the map
function set_map_click(map){
    // Display latlng info for any place on the map when clicked
    function onMapClick(e) {
       L.popup()
        .setLatLng(e.latlng)
        .setContent(e.latlng.toString())
        .openOn(map);
    }
    // Trigger onMapClick function whenever map is clickeddb_id
    map.on('click', onMapClick);
}


$(document).ready(function(){
    map = make_map('map');
    add_tile_to(map);

    flickety_init();

    var all_layers_group = L.geoJson(features,{});
    var all_layers = all_layers_group.getLayers();
    all_layers.forEach(function(layer){
        layer.bindPopup(layer.feature.properties.db_id.toString());
        layer.on({
            click: whenClicked
        });
    });

    var points = all_layers.filter(function(lay){return lay.feature.geometry.type == "Point"});
    var zones = all_layers.filter(function(lay){return lay.feature.geometry.type == "Polygon"});

    zones.forEach(function(zone){
        zone.setStyle({
              weight: 1,
              //color: zone.feature.properties['marker-color'],
              dashArray: '',
              fillOpacity: 0.3
        });
    });

    points.forEach(function(point){
        point.setIcon(icon_objs[point.feature.properties.icon]);
    })

    // Set layers and add toggle control menu for each layer
    var overlays = {};
    LAYER_FIELDS.forEach(function(lay_name){
        var lays = all_layers.filter(function(lay){return lay.feature.properties.layer == lay_name});
        var laygroup = L.layerGroup(lays);
        laygroup.addTo(map);
        overlays[lay_name] = laygroup;
    });

    L.control.layers(null, overlays).addTo(map);

    set_map_click(map);

    // Use GPS to locate you on the map and keeps watching
    // your location. Set to watch: true to have it watch location.
    map.locate({watch: false});

    // Current solution to keep geoLocation only
    // relevant in the campus/canyon area is to set
    // map bounds. Not the ideal solution, but I think
    // it will work for now.

    // NOTE: GETS REAL WEIRD AND JUMPY IN SAFARI
    // However, works fine in Google Chrome

    var northWest = L.latLng(45.48469, -122.63892);
    var southEast = L.latLng(45.47897, -122.62268);
    var bounds = L.latLngBounds(northWest, southEast);

    map.setMaxBounds(bounds);

    function onLocationFound(e) {
      // If you are within the campus bounds, the map
      // *should* center on your location and add a marker
      // where you are.
      if (bounds.contains(e.latlng)) {
        map.setView(e.latlng, 18); // Set view to location and zoom in
        var radius = e.accuracy / 2;

        L.marker(e.latlng, {icon: locateIcon}).addTo(map)
          .bindPopup("You are within " + radius + " meters from this point").openPopup();

        L.circle(e.latlng, radius).addTo(map);

      }
      // If you are not on campus, the map should not care
      // about your location, and it will just center on the
      // canyon, leaving no marker of where you are
      else {
        map.setView([lat_setting,long_setting], initial_zoom);
      }

    }
    map.on('locationfound', onLocationFound);


    // Error if locating fails
    function onLocationError(e) {
      alert(e.message);
    }

    map.on('locationerror', onLocationError);
});
