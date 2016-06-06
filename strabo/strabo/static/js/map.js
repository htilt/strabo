
var map = L.map('map'
).setView([lat_setting, long_setting], 17);

L.tileLayer(tile_src, {
  attribution: tile_attr1,
  minZoom: 14, //increased min zoom to see Willamette river
  maxZoom: 22,
  ext: extension
}).addTo(map);




// add pre-existing points, zones, and lines to map
// interest_points, zones, and lines variables from the
// interest_points.js file
var point_features = L.geoJson(interest_points, {
  onEachFeature: onEachPoint,
}).addTo(map);

var zone_features = L.geoJson(interest_zones, {
  onEachFeature: onEachZone
}).addTo(map);

var line_features = L.geoJson(interest_lines, {
  onEachFeature: onEachLine,
}).addTo(map);

// set styles and popups for zones
function onEachZone(feature, layer) {
  layer.bindPopup(feature.geometry.db_id);
  layer.setStyle({
        weight: 1,
        color: feature.properties['marker-color'],
        dashArray: '',
        fillOpacity: 0.3
  });
  layer.on({
      click: whenClicked
  });
}
// set styles and popups for lines
function onEachLine(feature, layer) {
  layer.bindPopup(feature.geometry.db_id);
  layer.setStyle({
        weight: 4,
        color: feature.properties['marker-color'],
        dashArray: '',
  });
  layer.on({
      click: whenClicked
  });
}
// set styles and popups for points
function onEachPoint(feature, layer) {
  layer.bindPopup(feature.geometry.db_id);
  // layer.setIcon(feature.properties['icon']);
  layer.on({
      click: whenClicked
  });
}

// Set layers and add toggle control menu for each layer
// (upper rh corner of map)
var overlays = {
  "Points": point_features,
  "Lines": line_features,
  "Zones": zone_features,
}
var controlLayers = L.control.layers(null, overlays).addTo(map);

// Display the id of an interest point when clicked
function whenClicked(e) {
  // e = event
  var db_id=e.target.feature.geometry.db_id;
  see_ip(db_id);
}

// Display latlng info for any place on the map when clicked
var popup = L.popup();
function onMapClick(e) {
  popup
    .setLatLng(e.latlng)
    .setContent(e.latlng.toString())
    .openOn(map);
}

// Trigger onMapClick function whenever map is clickeddb_id
map.on('click', onMapClick);

//this function loads the text and images associated
//with a selected interest point
function see_ip(db_id) {
    //in every other thing bug, this is never called
    $.post(
    "/map/post",
    {db_id:db_id},
    function(data){console.log("post callback called!");}
    );
}
