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
function centerLocation(map,latlng,bounds){
    if (bounds.contains(latlng)) {
        map.setView(latlng, 18); // Set view to location and zoom in
    }
}
var CenterControl = L.Control.extend({
    //
    //taken from the leafelet docs using the Zoom control as a basis
    //
    initialize: function (bounds,options) {
        this.centerBounds = bounds
        this.latLng = null
        L.Util.setOptions(this, options);
    },
    onAdd: function (map) {
        // create the control container with a particular class name
        var $container = $('<div class="leaflet-control-zoom leaflet-bar"></div>');
        $container.html('<a class="leaflet-control-zoom-in focus_button">&#9679;</a>');
        var mythis = this;

		$container
		    .on('click', L.DomEvent.stopPropagation)
		    .on('mousedown', L.DomEvent.stopPropagation)
		    .on('dblclick', L.DomEvent.stopPropagation)
		    .on('click', L.DomEvent.preventDefault)
            .on('click',map.getContainer().focus)
            .on('click',function(){
                console.log("clicked!!");
                console.log(mythis.latLng);
                if(!(mythis.latLng == null)){
                    console.log("clicked!!!!!!!!!!!!!!!s");
                    centerLocation(map,mythis.latLng,mythis.centerBounds);
                }
            })

        return $container[0];
    },
    locationGotten:function(latLng){
        console.log(latLng);
        console.log(this.centerBounds);
        this.latLng = latLng
    }
});

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

    var zoom_to = new CenterControl(bounds,{position:"topleft"});
    zoom_to.addTo(map);

    var location_was_found = false;
    function onLocationFound(e) {
      // If you are within the campus bounds, the map
      // *should* center on your location and add a marker
      // where you are.
      zoom_to.locationGotten(e.latlng);
      if (bounds.contains(e.latlng)) {
          centerLocation(map,e.latlng,bounds)
        var radius = e.accuracy / 2;

        L.marker(e.latlng, {icon: locateIcon}).addTo(map)
          .bindPopup("You are within " + radius + " meters from this point").openPopup();

        L.circle(e.latlng, radius).addTo(map);
      }
      else{
          if(location_was_found){
              map.setView([straboconfig["LAT_SETTING"], straboconfig["LONG_SETTING"]], straboconfig["INITIAL_ZOOM"]);
          }
      }
      location_was_found = true;
    }
    map.on('locationfound', onLocationFound);


    // Error if locating fails
    function onLocationError(e) {
        alert(e.message);
    }

    map.on('locationerror', onLocationError);
});
