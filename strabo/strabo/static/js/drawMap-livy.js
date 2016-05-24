// instantiate a Leaflet map object in the correct div
// 'drawMap'. Set lat, lng for the map's center
var drawMap = L.map('drawMap', {
}).setView([lat_setting, long_setting], 12 );

// if you wish to use map tiles that take other or more variables,
// you will need to add those below.
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
  maxZoom: 18,
  attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
    '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
    'Imagery © <a href="http://mapbox.com">Mapbox</a>',
  id: 'mapbox.streets',
}).addTo(drawMap);

// add pre-existing points, zones, and lines to map
// interest_points, zones, and lines variables from the
// interest_points.js file
var point_features = L.geoJson(interest_points, {
  onEachFeature: onEachPoint,
}).addTo(drawMap);

var zone_features = L.geoJson(interest_zones, {
  onEachFeature: onEachZone
}).addTo(drawMap);

var line_features = L.geoJson(interest_lines, {
  onEachFeature: onEachLine,
}).addTo(drawMap);

// set styles and popups for zones
function onEachZone(feature, layer) {
  layer.bindPopup(feature.geometry.name);
  layer.setStyle({
        weight: 1,
        color: feature.properties['marker-color'],
        dashArray: '',
        fillOpacity: 0.3
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
}
// set styles and popups for points
function onEachPoint(feature, layer) {
  layer.bindPopup(feature.geometry.name);
  // layer.setIcon(feature.properties['icon']);
}

var drawnItems = new L.FeatureGroup();
drawMap.addLayer(drawnItems);

// Initialise the draw control and pass it the FeatureGroup of editable layers
// Removes some toolbar things and also sets colors

var shapeColorInit = '#2397EB';

var options1 = {

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

var options2 = {
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

var drawControla = new L.Control.Draw(options1);
var drawControlb = new L.Control.Draw(options2);



drawMap.addControl(drawControla);


var obJSON; ////// THIS IS THE OBJECT U WANT
var shapeLayer;

drawMap.on('draw:created', function (e) { //grabs layer of drawn item
  var type = e.layerType;
  shapeLayer = e.layer;
  //if the layer type is a circle / marker, then we only have one set of latlngs to deal with, therefore different formula
  if (type === 'polyline') {
    drawnItems.addLayer(shapeLayer);
    obJSON = shapeLayer.toGeoJSON(); //creates JSON object
  }
  else if (type === 'marker') {
    drawnItems.addLayer(shapeLayer);
    obJSON = shapeLayer.toGeoJSON();
  }
  else if (type === 'polygon') {
    obJSON = shapeLayer.toGeoJSON();
   	drawnItems.addLayer(shapeLayer);
  }

  drawControla.removeFrom(drawMap);
  drawMap.addControl(drawControlb);
})

drawMap.on('draw:deletestop', function (e) {
  drawControlb.removeFrom(drawMap);
  drawMap.addControl(drawControla);

})


drawMap.on('draw:edited', function (e) {

  var editLayers = e.layers;
  var type = e.layerType;




  editLayers.eachLayer(function (layer) {
    obJSON = layer.toGeoJSON();
    console.log(obJSON);
    console.log(shapeLayer);
    //shapeLayer.setStyle({color:'#2397EB'});
    //layer.setStyle({color:'#2397EB'})
    });
})

$(function()
{
  var $e = $("#colorPick")
  var $usrSelect = $("#colorPick :selected").text()
  console.log($usrSelect);

  $e.change(function() {
    $usrSelect = $("#colorPick :selected").text();
    console.log($usrSelect);





  //console.log($dropDown);

    //var menuNum = this.value;
    //var menuParent = $('btn btn-default dropdown-toggle');
    //var msg = '';

    switch($usrSelect) {
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
      case "Red":
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

$('#upload-btn').click(function (e) {
  console.log(obJSON);
  var JSONobject = JSON.stringify(obJSON);
  console.log(JSONobject);
  $('#geojson-field').attr("value", JSONobject);
});


  // Returns an array of the points in the path.


       // need to write a function which updates this array if the points are edited.

    // process latLngs as you see fit and then save
