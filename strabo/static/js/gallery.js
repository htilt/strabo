var main = function() {
  // Fade image in gallery in or out when user mouses over
  $(".img-responsive").mouseover(function() {
    $(this).addClass("show-metadata");
  });

  $(".img-responsive").mouseout(function() {
    $(this).removeClass("show-metadata");
  });
  
  // ELIMINATE?
  // $("[rel='tooltip']").tooltip();

  // Display caption over image with hover
  $('.thumbnail').hover(
      function(){
          $(this).find('.caption').fadeIn(250); //.fadeIn(250)
      },
      function(){
          $(this).find('.caption').fadeOut(250); //.fadeOut(205)
      }
  ); 

  var $lightbox = $('#lightbox');

  // Toggle lightbox with user click on image
  $('[data-target="#lightbox"]').on('click', function(event) {
      // Find the clicked image's metadata, src, etc.
      var $img = $(this).find('img'), 
         src = $img.data('fullsrc'),
         alt = $img.attr('alt'),
         metadata = $(this).find('.img-metadata p').clone(),
         css = {
             'maxWidth': $(window).width() - 150,
             'maxHeight': $(window).height() - 100
         };
     // Set lightbox to reflect the image's metadata, src, etc.
     $lightbox.find('.close').addClass('hidden');
     $lightbox.find('img').attr('src', src);
     $lightbox.find('img').attr('alt', alt);
     $('.modal-metadata p').html(metadata)
     $lightbox.find('img').css(css);
  });
  // Set lightbox to be sixed to image, show x button
  $lightbox.on('shown.bs.modal', function (e) {
    var $img = $lightbox.find('img');           
    $lightbox.find('.modal-dialog').css({'width': $img.width()});
    $lightbox.find('.close').removeClass('hidden');
  });

};

$(document).ready(main);