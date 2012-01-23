if(!malica) {
	var malica = {};
}

/**
 * The ImageResizer takes in a list of images (jquery selected) and a max dimension
 * and resizes them if needed to the max dim
 * !! Images must be visibility hidden in the page for this to work
 */
malica.ImageResizer = function($images) {
	this._$images = $images;
};
/**
 * Will resize the set of images while they are loading by making sure they are really
 * done loading and then checking their sizes.
 * !! Images must be visibility hidden in the page for this to work
 */
malica.ImageResizer.prototype.resizeOnPageLoad = function(maxDim, noResizeIfSmaller) {
	var self = this;
	this._$images.each(function() {
		var photo = this;
		var img = new Image();
		img.addEventListener('load', function() {
			photo._size = {
				w: photo.width,
				h: photo.height
			};
			// Resize a photo to the max dim but not if smaller
			self._resizeAPhoto(photo, maxDim, noResizeIfSmaller);
		}, false);
		img.src = photo.src;
	});	
};
malica.ImageResizer.prototype.resizeAgain = function(maxDim, noResizeIfSmaller) {
	var self = this;
	this._$images.each(function() {
		self._resizeAPhoto(this, maxDim, noResizeIfSmaller);
	});
};
malica.ImageResizer.prototype._resizeAPhoto = function(photo, maxDim, noResizeIfSmaller) {
	if(photo._size.w < 50 && photo._size.h < 50) {
		photo.style.display = "none";
	} else if(photo._size.w > 1000 || photo._size.h > 1000) {
		photo.style.display = "none";
	} else {
		if(noResizeIfSmaller && photo._size.w < maxDim && photo._size.h < maxDim) {
			photo.style.visibility = "visible";
		} else {
			malica.ImageResizer.resize(photo, photo._size.w, photo._size.h, maxDim);
			photo.style.visibility = "visible";
		}
	}
};
malica.ImageResizer.resize = function(photo, originalW, originalH, maxDim) {
	//photo.height = photo.width = null;
	if(originalW > originalH) {
		photo.width = maxDim;
	} else {
		photo.height = maxDim;
	}
};