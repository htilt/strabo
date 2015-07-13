var main = function() {
  $('.dropdown-toggle').click(function() {
    $('.dropdown-menu').toggle();
  });
  
  $('.interest-point').click(function() {
    $('.gallery').toggle();
  });
}

$(document).ready(main);