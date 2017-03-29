$(document).ready(function () {
  	$('a.dropdown').focus(function() {
	    $('ul.dropdown-menu').addClass("expanded");
	    $('a.dropdown').addClass("active");
  });

  $('a.dropdown').blur(function() {
    $('ul.dropdown-menu').removeClass("expanded");
    $('a.dropdown').removeClass("active");
  });
});
