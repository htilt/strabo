var map = L.map('map').setView([45.48174, -122.631], 17);
//var user_location = map.locate({setView:true, maxZoom:16});

L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
  maxZoom: 18,
  attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
    '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
    'Imagery © <a href="http://mapbox.com">Mapbox</a>',
  id: 'mapbox.streets'
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

/*
$.get("/interest_points", function(data)) {
  geojson = L.geoJson(data, {
    onEachFeature: onEachFeature
  }).addTo(map);
}
*/

geojson = L.geoJson(interest_points, {
  onEachFeature: onEachFeature
}).addTo(map);

var popup = L.popup();

function onMapClick(e) {
  popup
    .setLatLng(e.latlng)
    .setContent(e.latlng.toString())
    .openOn(map);
}

map.on('click', onMapClick);


