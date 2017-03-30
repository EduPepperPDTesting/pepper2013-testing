$(document).ready(function () {
  	$('#dropdown').click(function(event) {
	    $('ul.dropdown-menu').addClass("expanded");
	    $('#dropdown').addClass("active");
	    $(document).one("click", function(){
    		$('ul.dropdown-menu').removeClass("expanded");
    		$('#dropdown').removeClass("active");
    });
	    event.stopPropagation();
  });
});
