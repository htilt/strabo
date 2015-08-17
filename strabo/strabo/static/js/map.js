var map = L.map('map', {
  maxBounds: [
  //southWest
  [45.4793, -122.6416],
  //northEast
  [45.48409, -122.62264]
  ],
}).setView([45.48174, -122.631], 17 );

//var user_location = map.locate({setView:true, maxZoom:16});

L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
  maxZoom: 18,
  attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
    '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
    'Imagery © <a href="http://mapbox.com">Mapbox</a>',
  id: 'mapbox.streets',

}).addTo(map);

// add points, zones, and lines to map
var point_features = L.geoJson(interest_points, {
  onEachFeature: onEachFeature
}).addTo(map);

var zone_features = L.geoJson(interest_zones, {
  onEachFeature: onEachFeature
}).addTo(map);

var line_features = L.geoJson(interest_lines, {
  onEachFeature: onEachFeature
}).addTo(map);

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

function onEachFeature(feature, layer) {
  layer.bindPopup(feature.geometry.name)
  //bind click
  layer.on({
      click: whenClicked
  });
}

var popup = L.popup();

function onMapClick(e) {
  popup
    .setLatLng(e.latlng)
    .setContent(e.latlng.toString())
    .openOn(map);
}

map.on('click', onMapClick);
