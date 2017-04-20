/*$(window).load(function() {
	// Animate loader off screen
	$(".se-pre-con").fadeOut(5300);
});*/
selectedItems=0;
$(document).on('click', '.col-md-15', function() {
	//alert($(this).hasClass('clicked'));
	alert();
	if ($(this).hasClass('clicked')) {
		$('.selected-description').text(--selectedItems);
	} else {
		$('.selected-description').text(++selectedItems);
	}
	$(this).toggleClass('clicked');
	$('.selected-description').css('font-style', 'bold');
});
