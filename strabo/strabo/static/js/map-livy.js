var map = L.map('map',
{
  maxBounds: [
  //southWest
  [41.891206, 12.426391],
  //northEast
  [41.899312, 12.528788]
  ],
}
).setView([41.882695, 12.495142], 14 );

//var user_location = map.locate({setView:true, maxZoom:16});

L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
  maxZoom: 18,
  attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
    '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
    'Imagery © <a href="http://mapbox.com">Mapbox</a>',
  id: 'mapbox.streets',

}).addTo(map);

// var imageUrl = 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Plan_of_the_Hills_of_Ancient_Rome.jpg/1280px-Plan_of_the_Hills_of_Ancient_Rome.jpg',
//     imageBounds = [[41.86209, 12.448391], [41.921312, 12.518788]];

// L.imageOverlay(imageUrl, imageBounds).addTo(map);

// add pre-existing points, zones, and lines to map
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
  layer.bindPopup(feature.geometry.name);
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
  layer.bindPopup(feature.geometry.name);
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
  layer.bindPopup(feature.geometry.name);
  // layer.setIcon(feature.properties['icon']);
  layer.on({
      click: whenClicked
  });
}

var overlays = {
  "Points": point_features,
  "Lines": line_features,
  "Zones": zone_features,
}

var controlLayers = L.control.layers(null, overlays).addTo(map);

function whenClicked(e) {
  // e = event
  console.log(e.target.feature.geometry.name);
  var name=e.target.feature.geometry.name;
  $.post(
    "/map/post", 
    {key:name},
    function(data) {
      $("#img-wrapper").html(data)
    }
    );
}

var popup = L.popup();

function onMapClick(e) {
  popup
    .setLatLng(e.latlng)
    .setContent(e.latlng.toString())
    .openOn(map);
}

map.on('click', onMapClick);
