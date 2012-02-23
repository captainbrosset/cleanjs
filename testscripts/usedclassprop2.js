// this is a fricking test
(function() {
	var MyClass = function(wow) {
		this._horizontal = null;
		this.posY = 6;
	};
	MyClass.prototype = {
		init : function(evt) {
			var offsetY = this._horizontal ? 0 : evt.clientY - this.posY;
			return offsetY;
		}
	};
	return new MyClass();
})();