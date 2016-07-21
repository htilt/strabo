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

function centerLocation(map,latlng,bounds){
    /*
    Centers location on latlng and zooms to specified level if latlng is in bounds,
    else it zooms to an overview of the whole canyon.
    */
    if (bounds.contains(latlng)) {
        map.setView(latlng, straboconfig['IN_CANYON_ZOOM']); // Set view to location and zoom in
    }
    else{
        map.setView([straboconfig["LAT_SETTING"], straboconfig["LONG_SETTING"]], straboconfig["INITIAL_ZOOM"]);
    }
}
var CenterControl = L.Control.extend({
    //
    //see leafelet IControl docs for more details on interface.
    //
    initialize: function (bounds,options) {
        this.centerBounds = bounds
        this.latLng = null
        L.Util.setOptions(this, options);
    },
    onAdd: function (map) {
        /*
        Creates an html div that is the button icon.

        Then sets click events on that div so that it center the image and does not do anything else.

        Much of this is taken directly from the leaflet source code L.Control.Zoom declaration
        */
        var html_img_code = "&#9679";
        var $container = $('<div class="leaflet-control-zoom leaflet-bar"></div>');
        $container.html('<a class="leaflet-control-zoom-in focus_button">'+html_img_code+'</a>');

        var mythis = this;//hackish way to get ``this`` into the internal function.

		$container
		    .on('click', L.DomEvent.stopPropagation)
		    .on('mousedown', L.DomEvent.stopPropagation)
		    .on('dblclick', L.DomEvent.stopPropagation)
		    .on('click', L.DomEvent.preventDefault)
            .on('click',map.getContainer().focus)
            .on('click',function(){
                if(!(mythis.latLng == null)){
                    centerLocation(map,mythis.latLng,mythis.centerBounds);
                }
            })

        return $container[0];
    },
    locationFound:function(latLng){
        //updates internal latlng position so that it is the most recent version.
        this.latLng = latLng
    }
});
var LocationGraphic = function(){
    /*
    This object represents the marker that shows a person's location.
    */
    this.marker = null;
    this.circle = null;
    this.removeGraphicsFrom =  function(map){
        /*
        if graphic is on the map, it is removed
        */
        if(this.marker != null){
            map.removeLayer(this.marker);
            this.marker = null;
        }
        if(this.circle != null){
            map.removeLayer(this.circle);
            this.circle = null;
        }
    }
    this.addGraphicsTo = function(map,latlng,accuracy){
        /*
        adds graphic to the map at latlng
        */
        var radius = accuracy / 2;

        this.marker = L.marker(latlng, {icon: locateIcon}).addTo(map);
        //                .bindPopup("You are within " + radius + " meters from this point").openPopup();

        this.circle = L.circle(latlng, radius).addTo(map);
    }
}
function set_geolocation(map){
    /*
    Geolocation operates in the following way:

    The first time location of the device is found, the map centers on that location (or the center of the canyon if the location is not in the bounds).

    Any time afterwards, when the browser updates your geolocation, it changes the marker marking your location on the map and updates a value storing the latlng position of the device, but does not center the picture.

    When you click the center button, it zooms to the latest latlng position.
    */

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
    var location = new LocationGraphic(bounds);

    var location_was_found = false;
    function onLocationFound(e) {
        zoom_to.locationFound(e.latlng);

        if(!location_was_found){
            centerLocation(map,e.latlng,bounds)
        }
        location_was_found = true;

        location.removeGraphicsFrom(map);
        if (bounds.contains(e.latlng)) {
            location.addGraphicsTo(map,e.latlng,e.accuracy);
        }
    }
    map.on('locationfound', onLocationFound);


    // Error if locating fails
    function onLocationError(e) {
        console.log(e.message);
        alert(e.message);
    }

    map.on('locationerror', onLocationError);

    // Use GPS to locate you on the map and keeps watching
    // your location. Set to watch: true to have it watch location.
    map.locate({watch: true});
}
