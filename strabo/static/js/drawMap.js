var shape_drawn = false;
var shapeLayer;

function init_map(){
    /*
    Creates and configures the admin map and adds the interest points to it.

    Returns the map.
    */
    var drawMap = make_map('drawMap');
    add_tile_to(drawMap);


    var all_layers_group = L.geoJson(features);
    set_styles(all_layers_group);
    bind_popups(all_layers_group);
    all_layers_group.addTo(drawMap);
    return drawMap;
}
function set_draw_controls(drawMap,drawnItems){
    /*
    Sets controls which allow one to add a polygon or a point. The control mechanics
    (options and events) conspire to create an editing enviornment where only
    one feature can ever be placed on the map in one form. The form control the ensures
    that at least one feature was placed, so that exactly one feature will be submitted
    with the interest point, as desired.
    */

    var shapeColorInit = '#2397EB';
    var addControl = new L.Control.Draw({
        draw : {
          polyline: false,
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

    var editControl = new L.Control.Draw({
      draw: false,

      edit: {
          featureGroup: drawnItems,
          edit: {
            selectedPathOptions: {
              color: 'red'
            }
          }
        }
    });
    if(edit_json){
        drawMap.addControl(editControl);
    }
    else{
        drawMap.addControl(addControl);
    }


    drawMap.on('draw:created', function (e) { //grab s layer of drawn item
        shapeLayer = e.layer;
        shape_drawn = true;
        drawnItems.addLayer(shapeLayer);

        addControl.removeFrom(drawMap);
        drawMap.addControl(editControl);
    })

    drawMap.on('draw:deleted', function (e) {
        //hackish way of finding out if there were any objects
        //that were actually deleted. Tested with leaflet 0.7.7 and leaflet-draw 0.2.3
        //probably should be retested on package upgrade
        var objs_deleted = Object.keys(e.layers._layers);
        if (objs_deleted.length > 0){
            shape_drawn = false;

            editControl.removeFrom(drawMap);
            drawMap.addControl(addControl);
        }
    })
}
function init_geojson_setter(drawnItems){
    if (edit_json){
        shape_drawn = true;
        shapeLayer = L.geoJson(edit_json).getLayers()[0];
        shapeLayer.addTo(drawnItems);
        shapeLayer.bindPopup("You are editing this point.").openPopup()
    }
    $('#upload-btn').click(function (e) {
        var JSONobject = shape_drawn ? JSON.stringify(shapeLayer.toGeoJSON()) : "";
        $('#geojson-field').attr("value", JSONobject);
    });
}
$(function(){
    var drawMap = init_map();

    var drawnItems = new L.FeatureGroup();
    drawMap.addLayer(drawnItems);
    init_geojson_setter(drawnItems)
    set_draw_controls(drawMap,drawnItems)
});
