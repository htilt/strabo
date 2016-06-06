
var map = L.map('map'
).setView([lat_setting, long_setting], 17);

L.tileLayer(tile_src, {
  attribution: tile_attr1,
  minZoom: 14, //increased min zoom to see Willamette river
  maxZoom: 22,
  ext: extension
}).addTo(map);




// add pre-existing points, zones, and lines to map
// interest_points, zones, and lines variables from the
// interest_points.js file
var point_features = L.geoJson(interest_points, {
  onEachFeature: onEachPoint,
}).addTo(map);

var zone_features = L.geoJson(interest_zones, {
  onEachFeature: onEachZone
}).addTo(map);

var line_features = L.geoJson(interest_lines, {
  onEachFeature: onEachLine,
}).addTo(map);

// set styles and popups for zones
function onEachZone(feature, layer) {
  layer.bindPopup(feature.geometry.db_id);
  layer.setStyle({
        weight: 1,
        color: feature.properties['marker-color'],
        dashArray: '',
        fillOpacity: 0.3
  });
  layer.on({
      click: whenClicked
  });
}
// set styles and popups for lines
function onEachLine(feature, layer) {
  layer.bindPopup(feature.geometry.db_id);
  layer.setStyle({
        weight: 4,
        color: feature.properties['marker-color'],
        dashArray: '',
  });
  layer.on({
      click: whenClicked
  });
}
// set styles and popups for points
function onEachPoint(feature, layer) {
  layer.bindPopup(feature.geometry.db_id);
  // layer.setIcon(feature.properties['icon']);
  layer.on({
      click: whenClicked
  });
}

// Set layers and add toggle control menu for each layer
// (upper rh corner of map)
var overlays = {
  "Points": point_features,
  "Lines": line_features,
  "Zones": zone_features,
}
var controlLayers = L.control.layers(null, overlays).addTo(map);

// Display the id of an interest point when clicked
function whenClicked(e) {
  // e = event
  var db_id=e.target.feature.geometry.db_id;
  console.log(db_id);
  see_ip(db_id);
}

// Display latlng info for any place on the map when clicked
var popup = L.popup();
function onMapClick(e) {
  popup
    .setLatLng(e.latlng)
    .setContent(e.latlng.toString())
    .openOn(map);
}

// Trigger onMapClick function whenever map is clicked
map.on('click', onMapClick);

//this function loads the text and images associated
//with a selected interest point
function see_ip(db_id) {
    //shrink map
    $('#map').removeClass('col-md-12');
    $('#map').addClass('col-md-9');
    //show text box
    $('#text-selection').removeClass('hidden');
    //show gallery
    $('#gallery').removeClass('hidden');
    //hide previous image messages
    $("#img-placeholder").addClass('hidden')
    $('#no-img-msg').addClass('hidden')
    $('#link-wrapper').addClass('hidden')
    //hide anny previous images
    $(".portfolio-item").addClass('hidden')
    //remove img-metadata p divs
    $('.img-metadata').empty()

    //get info from server and manage four possible situations
    //(there are neither images nor text for an interest point,
    //there are images but

    ///
    $.post(
    "/map/post",
    {db_id:db_id},
    function(data){
        // show gallery and link to more images
        $('#link-wrapper').removeClass('hidden')
        //$("#img_id_msg").html(data['images'][0]['interest_point']+'.')
        //$("#ip_link").html("see more images of " + data['images'][0]['interest_point'] + '.')
        //$("#ip_link").attr("href", 'gallery?search_field=interest_point&search_term=' + data['images'][0]['interest_point'])
        $("#image-gallery").removeClass("hidden")
        // add images to page
        var thum_names = data['thumb_fnames']

        for (t_name in thum_names) {
          var img_id = 'thumb-' + t_name;
          var select_id = '#' + img_id;
          var $thumbnail = $(select_id);
          $thumbnail.removeClass('hidden');
          $thumbnail.find('img').attr("src", "./static/thumbnails/" + t_name);
          //$thumbnail.find('img').data("fullsrc", "./static/uploads/" + data['images'][image]['filename'])
          //add metadata to images
          //$thumbnail.find('.img-metadata').append("<p>Title: "+data['images'][image]['title']+"</p>")
        }
      }
    );
}
