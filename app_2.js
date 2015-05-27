var main = function() {
  $('.dropdown-toggle').click(function() {
    $('.dropdown-menu').toggle();
  });
   
   
   $('.gallery-child').hide();
   
   /*
   $('#ip-2').hide();
   $('#ip-3').hide();
   $('#ip-4').hide();
	*/
	
  /*
  If the user clicks on a checkmark circle (id interest-point-1, etc.), toggle its respective gallery.
  */
  
  $('#interest-point-1').click(function() {
  	$('.gallery').toggle();
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