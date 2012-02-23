function Test () {
	var a = 1;
}
Test.prototype = {
	function1: function () {
		return this.toto;
	},
	function2: function () {
		this.toto = null;
	}
};