function toggleNav() {
	if ($('#myNav').height()  == 0){
		$("#myNav").css('height', '100%');
	} else {
		$("#myNav").css('height', '0');
 	}
	$('.menu-icon').toggleClass('text-dark text-light');
	$('.menu-icon').toggleClass('fa-bars fa-times');
}