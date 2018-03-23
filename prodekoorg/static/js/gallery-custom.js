
$(document).ready(function() {
	
	var imgView = $('.gallery-container .gallery-content #image-view').first();
	var imgTitle = $('.gallery-container .gallery-content > h1').first();
	var imgAlbum = $('.gallery-container .gallery-content > h2').first();
	
	
	if (imgView.length > 0 && imgTitle.length > 0 && imgAlbum.length > 0) {
		var newInfo = '<div class="image-info-custom"><h1 class="display-block">' + imgTitle.html() + '</h1><h2 class="display-block">' + imgAlbum.html() + '</h2></div>';
		$(newInfo).insertAfter(imgView);
	} else {
		if (imgTitle.length > 0) {
			$(imgTitle).addClass('display-block');
		}
		if (imgTitle.length > 0) {
			$(imgAlbum).addClass('display-block');
		}
	}
});