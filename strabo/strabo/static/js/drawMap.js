var drawMap = L.map('drawMap', {drawControl: true}, {
  maxBounds: [
  //southWest
  [45.4793, -122.6416],
  //northEast
  [45.48409, -122.62264]
  ],
}).setView([45.48174, -122.631], 17 );

L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
  maxZoom: 18,
  attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
    '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
    'Imagery © <a href="http://mapbox.com">Mapbox</a>',
  id: 'mapbox.streets',

}).addTo(drawMap);




// this is what grabs the coordinate data
drawMap.on('draw:created', function (e) {
    var type = e.layerType;
    var layer = e.layer;
    var latLngs;

    if (type === 'circle') {
       latLngs = layer.getLatLng();
       drawMap.addLayer(layer)
    }
    else
       latLngs = layer.getLatLngs();
   		drawMap.addLayer(layer);
       console.log(latLngs); // Returns an array of the points in the path.u75y76yy

    // process latLngs as you see fit and then save
})