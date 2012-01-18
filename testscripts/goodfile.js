var utils = {};
utils.Dom = function (id) {
	this._id = id;
};
utils.Dom.prototype = {
	getElement : function () {
		return document.getElementById(this._id);
	},
	setInnerHTML : function (content) {
		
		this._id.innerHTML = content;
	}
};