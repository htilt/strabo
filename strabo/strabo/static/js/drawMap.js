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

var shapeColorInit = '#2397EB';

var drawControl = new L.Control.Draw({
    
    draw : {
      polyline: {
        shapeOptions: {
          color: shapeColorInit
        }
      },
      polygon: {
        shapeOptions: {
          color: shapeColorInit
        }
      },
      circle: false,
      rectangle: false
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


var obJSON; ////// THIS IS THE OBJECT U WANT
var layer;


// this is what grabs the coordinate data when a shape is drawn
drawMap.on('draw:created', function (e) {
  //layer type just means what kind of shape
  var type = e.layerType;
  //every drawn items gets its own layer
  layer = e.layer;
  //if the layer type is a circle, then we only have one set of latlngs to deal with, therefore different formula
  if (type === 'polyline') {
    drawnItems.addLayer(layer);
    obJSON = layer.toGeoJSON();
    console.log(obJSON);
    //this is what injects the values into the HTML
  }
  else if (type === 'marker') {
    drawnItems.addLayer(layer);
    obJSON = layer.toGeoJSON();
    console.log(obJSON);
    
  }
  else if (type === 'polygon') {
    obJSON = layer.toGeoJSON();
    console.log(obJSON);
   	drawnItems.addLayer(layer);
  }
})


drawMap.on('draw:edited', function (e) {

  var editLayers = e.layers;
  var type = e.layerType;
  layer.setStyle({color:'#2397EB'});

  editLayers.eachLayer(function (layerShapes) {
    obJSON = editLayers.toGeoJSON();
    layerShapes.setStyle({color:'#2397EB'});
    console.log(obJSON);  //do whatever you want, most likely save back to db
    });


})

$(function()
{
  var $dropDown = $('li');

  $dropDown.on("click", function(event) {
    var menuNum = $(this).attr('id');

    switch(menuNum) {
      case 'menuItemOne' :
        L.geoJson(obJSON, {
          style: {
            "color": '#00A0B0'
          }
        });
        layer.setStyle({color:'#00A0B0'});
        break;
      case 'menuItemTwo' :
        L.geoJson(obJSON, {
          style: {
            "color": '#6A4A3C'
          }
        });
        layer.setStyle({color:'#6A4A3C'});
        break;
      case 'menuItemThree' :
        L.geoJson(obJSON, {
          style: {
            "color": '#CC333F'
          }
        });
        layer.setStyle({color:'#CC333F'});
        break;
      case 'menuItemFour' :
        L.geoJson(obJSON, {
          style: {
            "color": '#EB6841'
          }
        });
        layer.setStyle({color:'#EB6841'});
        break;
      case 'menuItemFive' :
        L.geoJson(obJSON, {
          style: {
            "color": '#8A9B0F'
          }
        });
        layer.setStyle({color:'#8A9B0F'});
        break
      default:
        break;
    }
  });
});



  // Returns an array of the points in the path.


       // need to write a function which updates this array if the points are edited.

    // process latLngs as you see fit and then save