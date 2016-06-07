// Initiates a Leaflet map

var map = L.map('map'
).setView([lat_setting, long_setting], initial_zoom);

L.tileLayer(tile_src, {
  attribution: tile_attr1,
  minZoom: 14,   //increased min zoom to see Willamette river
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
  onEachFeature: onEachZone,
}).addTo(map);

var line_features = L.geoJson(interest_lines, {
  onEachFeature: onEachLine,
}).addTo(map);



// set styles and popups for zones
function onEachZone(feature, layer) {
  layer.bindPopup(feature.geometry.db_id.toString());
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
  layer.bindPopup(feature.geometry.db_id.toString());
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
  layer.bindPopup(feature.geometry.db_id.toString());
  // layer.setIcon(feature.properties['icon']);
  layer.on({
      click: whenClicked
  });
}





// Set layers and add toggle control menu for each layer
var overlays = {
  "Interest Points": point_features,
  "Lines": line_features,
  "Zones": zone_features,
}
L.control.layers(null, overlays).addTo(map);







// Display the id of an interest point when clicked
function whenClicked(e) {
  see_ip(e.target.feature.geometry.db_id);
}

// Display latlng info for any place on the map when clicked
function onMapClick(e) {
   L.popup()
    .setLatLng(e.latlng)
    .setContent(e.latlng.toString())
    .openOn(map);
}



// Trigger onMapClick function whenever map is clickeddb_id
map.on('click', onMapClick);

//this function loads the text and images associated
//with a selected interest point
//example output:
// <div class="carousel-cell"><img src= "static/thumbnails/download.jpg"/></div><div class="carousel-cell"><img src= "static/thumbnails/download1.jpg"/></div><div class="carousel-cell"><img src= "static/thumbnails/download2.jpg"/></div>
function get_carosel_html(filename,descrip){
    var html = '<div class="carousel-cell">';
    html += '<img src= "static/thumbnails/' + filename + '"/>';
    html += '<p>' + descrip + '</p>';
    html += '</div>';
    return html;
}
function get_description_html(descrip){
    return '<p>' + descrip + '</p>';
}
function see_ip(db_id) {
    $.post(
        "/map/post",
        {db_id:db_id},
        function(imgs){
            var carousel_html = "";
            imgs.forEach(function(img){
                carousel_html += get_carosel_html(img.filename,img.description);
            });
            $("#carousel-holder").html(carousel_html);
        }
    );
    $('.popup').show();
    $('.container-popup').show();
}
function exit_button_clicked(){
    $('.popup').hide();
    $('.container-popup').hide();
}
