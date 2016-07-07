// Initialize custom GPS location icon
var locateIcon = L.icon({
    iconUrl: '/static/locationDot.png',
    iconSize: [20,20]
});

var ColorIcon = L.Icon.extend({
    options: {
        shadowUrl: '/static/map_icons/MapPinShadow.png',
        iconSize:     [30, 50],
        shadowSize:   [30, 32],
        iconAnchor:   [15, 50],
        shadowAnchor: [2, 30],
        popupAnchor:  [-3, -50]
    }
});

// Extract filename without extension (doesn't work for extensions
// longer than 4 characters)
function extractFileName(icon_name){
    return icon_name.slice(0,-4);
}

var icon_objs = function(){
    var icon_objs = {};
    MAP_ICONS.forEach(function(icon_name){
        icon_objs[icon_name] = new ColorIcon({iconUrl:'/static/map_icons/' + icon_name});
    });
    return icon_objs;
}();

// leaflet map object
function make_map(map_cont){
    var map = L.map(map_cont, {
    }).setView([lat_setting, long_setting], initial_zoom);

    return map;
}
function add_tile_to(map){
    L.tileLayer(tile_src,tile_attributes).addTo(map);
}
// sets icon object for points and stlying for zones
function set_styles(all_layers_group){
    var all_layers = all_layers_group.getLayers();

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
}
// Set layers and add toggle control menu for each layer
function place_overlays_on(all_layers_group,map){
    var all_layers = all_layers_group.getLayers();
    var overlays = {};
    LAYER_FIELDS.forEach(function(lay_name){
        var lays = all_layers.filter(function(lay){return lay.feature.properties.layer == lay_name});
        var laygroup = L.layerGroup(lays);
        laygroup.addTo(map);
        overlays[lay_name] = laygroup;
    });
    L.control.layers(null, overlays).addTo(map);
}
//makes it so that popups appear when clicked with the interest point database id
function bind_popups(all_layers_group){
    var all_layers = all_layers_group.getLayers();
    all_layers.forEach(function(layer){
        layer.bindPopup(layer.feature.properties.name);
    });
}
