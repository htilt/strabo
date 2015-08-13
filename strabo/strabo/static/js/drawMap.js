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
// Removes some toolbar things and also sets colors

var drawControl = new L.Control.Draw({
    
    draw : {
      polygon: {
        shapeOptions: {
          color: '#2397EB'
        }
      },
      circle: {
        shapeOptions: {
          color: '#2397EB'
        } 
      },
      rectangle: false,
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

//this grabs the HTML elements that get injected with lat and lng
var latCoordDump = document.getElementById('latitude');
var longCoordDump = document.getElementById('longitude');



// this is what grabs the coordinate data when a shape is drawn
drawMap.on('draw:created', function (e) {
  //layer type just means what kind of shape
  var type = e.layerType;
  //every drawn items gets its own layer
  var layer = e.layer;
  var latLngs;

  //if the layer type is a circle, then we only have one set of latlngs to deal with, therefore different formula
  if (type === 'circle') {
    latLngs = layer.getLatLng();
    drawnItems.addLayer(layer);
    var circleJSON = layer.toGeoJSON();
    console.log(circleJSON);
    //this is what injects the values into the HTML
    latCoordDump.value = latLngs.lat.toString();
    longCoordDump.value = latLngs.lng.toString();
  }
  else if (type === 'marker') {
    latLngs = layer.getLatLng();
    drawnItems.addLayer(layer);
    var markerJSON = layer.toGeoJSON()
    console.log(markerJSON)
    latCoordDump.value = latLngs.lat.toString();
    longCoordDump.value = latLngs.lng.toString();
    
  }
  else if (type === 'polygon') {
    latLngs = layer.getLatLngs(); // THIS IS THE ARRAY YOU WANT TO HARVEST  <<<<<<<<<<<<<<<<
    var polyJSON = layer.toGeoJSON();
    console.log(polyJSON);
   	drawnItems.addLayer(layer);

    for(i = 0; i < latLngs.length; i++) {

      var lats = [];
      var lngs = []; 
      lats.push(latLngs[i].lat);
      lngs.push(latLngs[i].lng);
    }
  }
})


drawMap.on('draw:edited', function (e) {

  var editLayers = e.layers;
  var type = e.layerType;

  editLayers.eachLayer(function (layer) {
    var editCoords = layer.getLatLngs();
    zoneLatLngs = editCoords;
    console.log(zoneLatLngs);   //do whatever you want, most likely save back to db
    });
})



  // Returns an array of the points in the path.


       // need to write a function which updates this array if the points are edited.

    // process latLngs as you see fit and then save