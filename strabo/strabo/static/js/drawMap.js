var drawMap = L.map('drawMap', { // sets the viewport location
  
  maxBounds: [
  //southWest
  [45.4793, -122.6416],
  //northEast
  [45.48409, -122.62264]
  ],
}).setView([45.48174, -122.631], 17 ); 

L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', { // gets map data
  maxZoom: 18,
  attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
    '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
    'Imagery © <a href="http://mapbox.com">Mapbox</a>',
  id: 'mapbox.streets',

}).addTo(drawMap); 


var point_features = L.geoJson(interest_points, { // these 3 variables add pre-existing points, zones, and lines to map
  onEachFeature: onEachPoint,
}).addTo(drawMap);

var zone_features = L.geoJson(interest_zones, {
  onEachFeature: onEachZone
}).addTo(drawMap);

var line_features = L.geoJson(interest_lines, {
  onEachFeature: onEachZone,
}).addTo(drawMap);


function onEachZone(feature, layer) { // this function attaches text to zones 
  layer.bindPopup(feature.geometry.name);
  layer.setStyle({
        weight: 1,
        color: feature.properties['marker-color'],
        dashArray: '',
        fillOpacity: 0.3
  });
}

function onEachPoint(feature, layer) { // this function attaches text to points
  layer.bindPopup(feature.geometry.name);
}

var drawnItems = new L.FeatureGroup(); // this variable contains items drawn in the current session
drawMap.addLayer(drawnItems); // this function adds the variable to the map

var shapeColorInit = '#2397EB'; // the default color for shapes and lines on the map

var options1 = { // this variable contains the feature set for draw mode
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
}

var options2 = { //this variable disables the feature set for draw mode
  draw: false,

  edit: {
      featureGroup: drawnItems,
      edit: {
        selectedPathOptions: {
          color: 'red'
        }
      }
    }

}

var drawControla = new L.Control.Draw(options1); //these two variables are used to toggle between enabling and disabling draw mode
var drawControlb = new L.Control.Draw(options2);



drawMap.addControl(drawControla); // by default, the map is in draw mode


var obJSON; // this variable will hold the user-created content
var shapeLayer; // this variable is used to as a layer to store all the user-created content



drawMap.on('draw:created', function (e) { //grabs layer of drawn item
  var type = e.layerType;
  shapeLayer = e.layer;
  
  if (type === 'polyline') { // these three conditions check the type of object
    drawnItems.addLayer(shapeLayer);
    obJSON = shapeLayer.toGeoJSON(); 
  }
  else if (type === 'marker') {
    drawnItems.addLayer(shapeLayer);
    obJSON = shapeLayer.toGeoJSON();    
  }
  else if (type === 'polygon') {
    obJSON = shapeLayer.toGeoJSON();
   	drawnItems.addLayer(shapeLayer);
  }

  drawControla.removeFrom(drawMap); // when a shape has been created, the map disables draw mode
  drawMap.addControl(drawControlb);
})

drawMap.on('draw:deletestop', function (e) { // if a shape is deleted, draw mode is renabled
  drawControlb.removeFrom(drawMap);
  drawMap.addControl(drawControla);

})


drawMap.on('draw:edited', function (e) { // updates the shape if it is edited
  
  var editLayers = e.layers;
  var type = e.layerType;

  editLayers.eachLayer(function (layer) {
    obJSON = layer.toGeoJSON();
    console.log(obJSON);
    console.log(shapeLayer);
    });
})

$(function() // this function allows the user to change the color of content
{
  var $e = $("#colorPick") // this function references the HTML base containing the dropdown list of colors
  var $usrSelect = $("#colorPick :selected").text()
  console.log($usrSelect);

  $e.change(function() {
    $usrSelect = $("#colorPick :selected").text();
    console.log($usrSelect); 
  


    switch($usrSelect) { // this switch applies a color based on the dropdown menu of possible options
      case 'Turqoise' :
        L.geoJson(obJSON, {
          style: {
            "color": '#00A0B0'
          }
        });
        shapeLayer.setStyle({color:'#00A0B0'}).addTo(drawMap);
        break;
      case 'Brown' :
        L.geoJson(obJSON, {
          style: {
            "color": '#6A4A3C'
          }
        });
        shapeLayer.setStyle({color:'#6A4A3C'});
        break;
      case "Father's Rage Red":
        L.geoJson(obJSON, {
          style: {
            "color": '#CC333F'
          }
        });
        shapeLayer.setStyle({color:'#CC333F'});
        break;
      case 'Orange' :
        L.geoJson(obJSON, {
          style: {
            "color": '#EB6841'
          }
        });
        shapeLayer.setStyle({color:'#EB6841'});
        break;
      case 'Green' :
        L.geoJson(obJSON, {
          style: {
            "color": '#8A9B0F'
          }
        });
        shapeLayer.setStyle({color:'#8A9B0F'});
        break
      default:
        break;
    }
  });
});

$('#upload-btn').click(function (e) { //this function stringifies the JSON object with correct color
  console.log(obJSON);
  var JSONobject = JSON.stringify(obJSON);
  console.log(JSONobject);
  $('#geojson-field').attr("value", JSONobject);
}); 