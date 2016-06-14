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

// Initialize color icons
var greenIcon = new ColorIcon({iconUrl: '/static/map_icons/MapPinGreen.png'});
var blueIcon = new ColorIcon({iconUrl: '/static/map_icons/MapPinBlue.png'});
var maroonIcon = new ColorIcon({iconUrl: '/static/map_icons/MapPinMaroon.png'});
var oliveIcon = new ColorIcon({iconUrl: '/static/map_icons/MapPinOlive.png'});
var orangeIcon = new ColorIcon({iconUrl: '/static/map_icons/MapPinOrange.png'});
var pinkIcon = new ColorIcon({iconUrl: '/static/map_icons/MapPinPink.png'});
var purpleIcon = new ColorIcon({iconUrl: '/static/map_icons/MapPinPurple.png'});
var tealIcon = new ColorIcon({iconUrl: '/static/map_icons/MapPinTeal.png'});
var yellowIcon = new ColorIcon({iconUrl: '/static/map_icons/MapPinYellow.png'});
var grayIcon = new ColorIcon ({iconUrl: 'static/map_icons/MapPinGray.png'});

// Initialize special icons
var sensitiveAreaIcon = new ColorIcon({iconUrl: '/static/map_icons/SensitiveAreaPin.png'});
var APIcon = new ColorIcon({iconUrl: '/static/map_icons/APicon.png'});

//leafelet map object
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
