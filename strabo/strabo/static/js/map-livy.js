var map = L.map('map'
// {
//   maxBounds: [
//   //southWest
//   [41.891206, 12.426391],
//   //northEast
//   [41.899312, 12.528788]
//   ],
// }
).setView([41.892695, 12.495142], 14 );

//var user_location = map.locate({setView:true, maxZoom:16});

L.tileLayer('http://stamen-tiles-{s}.a.ssl.fastly.net/watercolor/{z}/{x}/{y}.png', {
  attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  subdomains: 'abcd',
  minZoom: 1,
  maxZoom: 16,
  ext: 'png'
}).addTo(map);

// var imageUrl = 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Plan_of_the_Hills_of_Ancient_Rome.jpg/1280px-Plan_of_the_Hills_of_Ancient_Rome.jpg',
//     imageBounds = [[41.86209, 12.448391], [41.921312, 12.518788]];

// L.imageOverlay(imageUrl, imageBounds).addTo(map);

// add pre-existing points, zones, and lines to map
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

var overlays = {
  "Points": point_features,
  "Lines": line_features,
  "Zones": zone_features,
}

var controlLayers = L.control.layers(null, overlays).addTo(map);

function whenClicked(e) {
  // e = event
  console.log(e.target.feature.geometry.name);
  var name=e.target.feature.geometry.name;
  see_ip(name);
}

var popup = L.popup();

function onMapClick(e) {
  popup
    .setLatLng(e.latlng)
    .setContent(e.latlng.toString())
    .openOn(map);
}

map.on('click', onMapClick);

//this function loads the text and images associated
//with a selected interest points
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

    //get info from server
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
        $('#book_num').html("Book " + data['text-selection'][0]['book'])
        $('#section_num').html("Section " + data['text-selection'][0]['section'])
        $('#title').html(data['text-selection'][0]['name'])
        $('#attribution').html(data['text-selection'][0]['notes'])
      }
      //if there are both images and text
      else {
        // add content to text box
        $('#text').html(data['text-selection'][0]['passage'])
        $('#book_num').html("Book " + data['text-selection'][0]['book'])
        $('#section_num').html("Section " + data['text-selection'][0]['section'])
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

