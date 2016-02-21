// instantiate a Leaflet map object in the correct div
// 'map'. Set lat, lng for the map's center
var map = L.map('map'
).setView([lat_setting, long_setting], 14 );

// tile_src,  tile_attr1, subdomains, and extension are variables
// from the interest_points.js file
// if you wish to use different map tiles that take fewer variables, 
// you will need to eliminate the extra variables below for map
// tiles to load.
// if you wish to use map tiles that take other or more variables,
// you will need to add those below.
L.tileLayer(tile_src, {
  attribution: tile_attr1,
  subdomains: subdomains,
  minZoom: 1,
  maxZoom: 16,
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
  layer.bindPopup(feature.geometry.name);
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
  layer.bindPopup(feature.geometry.name);
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
  layer.bindPopup(feature.geometry.name);
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

// Display the name of an interest point when clicked
function whenClicked(e) {
  // e = event
  console.log(e.target.feature.geometry.name);
  var name=e.target.feature.geometry.name;
  see_ip(name);
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
function see_ip(name) {
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
    $.post(
    "/map/post", 
    {name:name},
    function(data) {
      //if there are neither images nor text      
      if (typeof data['text-selection'][0] === 'undefined' && typeof data['images'][0] === 'undefined') {
        //indicate there is no text
        $('#text').html('There is no passage associated with this location. Please select another.')
        $('#book_num').html('')
        $('#section_num').html('')
        $('#title').html('')
        $('#attribution').html('')
        //indicate there are no images
        $('#no-img-msg').removeClass('hidden')
      }
      //if there are images but no text
      else if (typeof data['text-selection'][0] === 'undefined') {
        //indicate lack of text
        $('#text').html('There is no passage associated with this location. Please select another.')
        $('#book_num').html('')
        $('#section_num').html('')
        $('#title').html('')
        $('#attribution').html('')
        // show gallery and link to more images
        $('#link-wrapper').removeClass('hidden')
        $("#img_id_msg").html(data['images'][0]['interest_point']+'.')
        $("#ip_link").html("see more images of " + data['images'][0]['interest_point'] + '.')
        $("#ip_link").attr("href", 'gallery?search_field=interest_point&search_term=' + data['images'][0]['interest_point'])
        $("#image-gallery").removeClass("hidden")
        // add images to page
        var images = data['images']

        for (image in images) {
          var img_id = 'thumb-' + image;
          var select_id = '#' + img_id;
          var $thumbnail = $(select_id);
          $thumbnail.removeClass('hidden')
          $thumbnail.find('img').attr("src", "./static/thumbnails-livy/" + data['images'][image]['thumbnail_name'])
          $thumbnail.find('img').data("fullsrc", "./static/uploads-livy/" + data['images'][image]['filename'])
          //add metadata to images
          $thumbnail.find('.img-metadata').append("<p>Title: "+data['images'][image]['title']+"</p>")
          
          if (data['images'][image]['date_created']) {
            $thumbnail.find('.img-metadata').append("<br><p>Date Created: "+data['images'][image]['date_created']+"</p><br>")
          }
          if (data['images'][image]['img_description']) {
            $thumbnail.find('.img-metadata').append("<p>Image Description: "+data['images'][image]['img_description']+"</p>")
          }
          if (data['images'][image]['notes']) {
            $thumbnail.find('.img-metadata').append("<p>Notes: "+data['images'][image]['notes']+"</p>")
          }
        }
      }
      //if there is text but no images
      else if (typeof data['images'][0] === 'undefined') {
        //indicate that there are no images
        $('#no-img-msg').removeClass('hidden')
        // add content to text box
        $('#text').html(data['text-selection'][0]['passage'])
        // if the admin has specified a book number, add it
        if (data['text-selection'][0]['book']) {
          $('#book_num').html("Book " + data['text-selection'][0]['book'])
        }
        else {
          $('#book_num').html("")
        }
        // if the admin has specified a section number, add it
        if (data['text-selection'][0]['section']) {
          $('#section_num').html("Section " + data['text-selection'][0]['section'])
        }
        else {
          $('#section_num').html("")
        }
        $('#title').html(data['text-selection'][0]['name'])
        $('#attribution').html(data['text-selection'][0]['notes'])
      }
      //if there are both images and text
      else {
        // add content to text box
        $('#text').html(data['text-selection'][0]['passage'])
        // if the admin has specified a book number, add it
        if (data['text-selection'][0]['book']) {
          $('#book_num').html("Book " + data['text-selection'][0]['book'])
        }
        else {
          $('#book_num').html("")
        }
        // if the admin has specified a section number, add it
        if (data['text-selection'][0]['section']) {
          $('#section_num').html("Section " + data['text-selection'][0]['section'])
        }
        else {
          $('#section_num').html("")
        }
        $('#title').html(data['text-selection'][0]['name'])
        $('#attribution').html(data['text-selection'][0]['notes'])
        // add images to page
        // show gallery and link to more images
        $('#link-wrapper').removeClass('hidden')
        $("#img_id_msg").html(data['images'][0]['interest_point']+'.')
        $("#ip_link").html("see more images of " + data['images'][0]['interest_point'] + '.')
        $("#ip_link").attr("href", 'gallery?search_field=interest_point&search_term=' + data['images'][0]['interest_point'])
        $("#image-gallery").removeClass("hidden")
        // add images to page
        var images = data['images']

        for (image in images) {
          var img_id = 'thumb-' + image;
          var select_id = '#' + img_id;
          var $thumbnail = $(select_id);
          $thumbnail.removeClass('hidden')
          $thumbnail.find('img').attr("src", "./static/thumbnails-livy/" + data['images'][image]['thumbnail_name'])
          $thumbnail.find('img').data("fullsrc", "./static/uploads-livy/" + data['images'][image]['filename'])
          //add metadata to images
          $thumbnail.find('.img-metadata').append("<p>Title: "+data['images'][image]['title']+"</p>")
          
          if (data['images'][image]['date_created']) {
            $thumbnail.find('.img-metadata').append("<br><p>Date Created: "+data['images'][image]['date_created']+"</p><br>")
          }
          if (data['images'][image]['img_description']) {
            $thumbnail.find('.img-metadata').append("<p>Image Description: "+data['images'][image]['img_description']+"</p>")
          }
          if (data['images'][image]['notes']) {
            $thumbnail.find('.img-metadata').append("<p>Notes: "+data['images'][image]['notes']+"</p>")
          }
        }
      }
    }
    );

}

//on close button, reset divs
$('#close-text').click(function(){
    //hide text box
    $('#text-selection').addClass('hidden')
    //expand map
    $('#map').removeClass('col-md-9')
    $('#map').addClass('col-md-12')
    //hide gallery and portfolio items (thumbnails)
    $('#gallery').addClass('hidden')
    $(".portfolio-item").addClass('hidden')
    //hide any previous image messages
    $('#link-wrapper').addClass('hidden')
    $('#no-img-msg').addClass('hidden')
    //add img message
    $("#img-placeholder").removeClass('hidden')
});

