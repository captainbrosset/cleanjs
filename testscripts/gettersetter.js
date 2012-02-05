var MyClass = function(prop) {
	this._prop = prop;
};
MyClass.prototype = {
	setup: function() {
		this.initSomeStuff();
	},

	initSomeStuff: function() {
		var test = document.getElementById("test");
		var self = this;
		test.onclick = function() {
			alert(self._prop)
		}
	},

	getProp: function() {
		return this._prop;
	},

	getty: function() {
		this.getty = tests;
	},

	setProp: function(prop) {
		this._prop = prop;
		return doSomething();
	}
};