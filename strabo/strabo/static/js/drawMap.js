// The Admin Map

var drawMap = L.map('drawMap', {
}).setView([lat_setting, long_setting], initial_zoom);

L.tileLayer(tile_src,tile_attributes).addTo(drawMap);




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


var myIcon = L.divIcon({
      className: 'my-div-icon',
      iconSize: [5, 5]
    });
    // layer.setIcon(feature.properties['icon']);
}

var drawnItems = new L.FeatureGroup();
drawMap.addLayer(drawnItems);

// Initialise the draw control and pass it the FeatureGroup of editable layers
// Removes some toolbar things and also sets colors

var shapeColorInit = '#2397EB';

var obJSON; ////// THIS IS THE OBJECT U WANT
var shapeLayer;

//for adding editing capability

if (edit_json){
    shapeLayer = L.geoJson(edit_json);
    obJSON = shapeLayer.toGeoJSON().features[0];
}

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

drawMap.on('draw:created', function (e) { //grab s layer of drawn item
    shapeLayer = e.layer;

    drawnItems.addLayer(shapeLayer);
    obJSON = shapeLayer.toGeoJSON();

    drawControla.removeFrom(drawMap);
    drawMap.addControl(drawControlb);
})

drawMap.on('draw:deleted', function (e) {
    //awkward, test this in different browsers
    if (Object.keys(e.layers._layers).length > 0){
        drawControlb.removeFrom(drawMap);
        drawMap.addControl(drawControla);
    }
})

drawMap.on('draw:edited', function (e) {
  var editLayers = e.layers;

  editLayers.eachLayer(function (layer) {
    obJSON = layer.toGeoJSON();
    //shapeLayer.setStyle({color:'#2397EB'});
    //layer.setStyle({color:'#2397EB'})
    });
})

$(function()
{
  var $e = $("#colorPick")
  var $usrSelect = $("#colorPick :selected").text();

  $e.change(function() {
    $usrSelect = $("#colorPick :selected").text();


  //console.log($dropDown);

    //var menuNum = this.value;
    //var menuParent = $('btn btn-default dropdown-toggle');
    //var msg = '';
    switch($usrSelect) {
      case 'Turquoise' :
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
        break;
      default:
        break;
    }
  });
});


$('#upload-btn').click(function (e) {
  var JSONobject = JSON.stringify(obJSON);
  $('#geojson-field').attr("value", JSONobject);
});


  // Returns an array of the points in the path.


       // need to write a function which updates this array if the points are edited.

    // process latLngs as you see fit and then save
