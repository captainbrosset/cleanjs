function Test() {
	this.property = 1;
	this.property2 = 5;
};
Test.prototype.doSomething = function() {
	var prop = this.property, ohyeah = 2;
	return prop + ohyeah;
};