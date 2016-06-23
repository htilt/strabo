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

var icon_objs = {};
MAP_ICONS.forEach(function(ico_name){
    icon_objs[ico_name] = new ColorIcon({iconUrl:'/static/map_icons/' + ico_name});
});

// leaflet map object
function make_map(map_cont){
    var map = L.map(map_cont, {
    }).setView([lat_setting, long_setting], initial_zoom);

    return map;
}
function add_tile_to(map){
    L.tileLayer(tile_src,tile_attributes).addTo(map);
}

// set styles and popups for zones
function makeOnEachZone(click_fn){
    return function(feature, layer) {
      layer.bindPopup(feature.geometry.db_id.toString());
      layer.setStyle({
            weight: 1,
            color: feature.properties['marker-color'],
            dashArray: '',
            fillOpacity: 0.3
      });
      layer.on({
          click: click_fn
      });
    }
}


function makeOnEachLine(click_fn){
// set styles and popups for lines
    return function (feature, layer) {
        layer.bindPopup(feature.geometry.db_id.toString());
        layer.setStyle({
            weight: 4,
            color: feature.properties['marker-color'],
            dashArray: '',
            fillOpacity: 1
        });
        layer.on({
          click: click_fn
        });
    }
}

function makeOnEachPoint(click_fn){
    // set styles and popups for points
    return function(feature, layer) {
      layer.bindPopup(feature.geometry.db_id.toString());
      layer.on({
          click: click_fn
      });
    }
}
