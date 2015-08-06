var drawMap = L.map('drawMap', {
  
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




var drawnItems = new L.FeatureGroup();
drawMap.addLayer(drawnItems);

// Initialise the draw control and pass it the FeatureGroup of editable layers
var drawControl = new L.Control.Draw({
    
    draw : {
      polygon: {
        shapeOptions: {
          color: 'blue'
        }
      },
      rect: false,
      polyline: false
    },


    edit: {
        featureGroup: drawnItems,
        edit: {
          selectedPathOptions: {
            color: 'red'
        }
      }
    }
});
drawMap.addControl(drawControl);

var zoneLatLngs;


// this is what grabs the coordinate data
drawMap.on('draw:created', function (e) {
  var type = e.layerType;
  var layer = e.layer;
  var latLngs;

  if (type === 'circle') {
    latLngs = layer.getLatLng();
    drawnItems.addLayer(layer);
  }
  else if (type === 'marker') {
    latLngs = layer.getLatLng();
    drawnItems.addLayer(layer);
  }
  else
    latLngs = layer.getLatLngs();
    zoneLatLngs = latLngs;
   	drawnItems.addLayer(layer);
    console.log(latLngs);
  })

  drawMap.on('draw:edited', function (e) {

  var editLayers = e.layers;
  var type = e.layerType;

  editLayers.eachLayer(function (layer) {
    var editCoords = layer.getLatLngs();
    zoneLatLngs = editCoords;
    console.log(zoneLatLngs);
    console.log(zoneLatLngs[0].lat);
        //do whatever you want, most likely save back to db
    });

})
  // Returns an array of the points in the path.


       // need to write a function which updates this array if the points are edited.

    // process latLngs as you see fit and then save