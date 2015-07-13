var main = function() {
  $('.dropdown-toggle').click(function() {
    $('.dropdown-menu').toggle();
  });
   
   $('.gallery-child').hide();

   $("#exit-gallery").click(function(){
    $('.gallery').hide()
   })

  $('.ip-check').click(function(){
    $(".gallery-child").hide();
    $(".gallery").show()
  })

  //to do (maybe): make this so it only selects the children of the interest point that's currently being looked at
  $('.thumbnails').children('img').mouseover(function(){
    var img = this
    var thumbnail_div = $(img).parent()
    var preview_div = $(thumbnail_div).siblings('.preview')
    var newimgsrc = $(img).attr('src')
    preview_div.children('img').attr('src', newimgsrc)
  })

  /*
  If the user clicks on a checkmark circle (id interest-point-1, etc.), toggle its respective gallery.
  */
  
  $('#interest-point-1').click(function() {
    $('#ip-1').toggle();
  });
  
  $('#interest-point-2').click(function() {
    $('#ip-2').toggle();
  });
  
  $('#interest-point-3').click(function() {
    $('#ip-3').toggle();
  });
  
  $('#interest-point-4').click(function() {
    $('#ip-4').toggle();
  });
}

$(document).ready(main);