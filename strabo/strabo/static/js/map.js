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


//defines zones 1 and 2
var zone1 = L.polygon([
    [45.48227, -122.63248],
    [45.48207, -122.6321],
    [45.48192, -122.63188],
    [45.48183, -122.63188],
    [45.48168, -122.63167],
    [45.48163, -122.63124],
    [45.48145, -122.63126],
    [45.48145, -122.6321],
    [45.48162, -122.63212],
    [45.48189, -122.63268],
],
  {
    //fillOpacity: 0.0,
  }
).addTo(map);

zone1.bindPopup("I love you.");

var zone2 = L.polygon([
    [45.48161, -122.63119],
    [45.48166, -122.63037],
    [45.48146, -122.63038],
    [45.48146, -122.63122],
],
  {
    //fillOpacity: 0.0,
  }
).addTo(map);


//groups zones into a group
var zones = L.layerGroup([zone1, zone2]);

//creates the overlay object
var overlayMaps = {
    "Zonez": zones
};
//uses the overaly object to make the little clicky selector in the top right 
L.control.layers(null, overlayMaps).addTo(map);



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


