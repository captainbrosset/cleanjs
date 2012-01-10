import re

class ClassData():
	"""Passed to each reviewer, as an element of the classes list, inside file_data.
	Instances of this class have the following attributes:
	- name: the name of the class (constructor function)
	- prototype: an array of names corresponding to functions and properties present in the prototype of the class
	- line_nb: the line number where the class constructor is defined
	You can then use the FunctionData in file_data.functions to get information about the constructor and other prototype functions of this class."""
	
	def __init__(self, name, prototype, line_nb):
		self.name = name
		self.prototype = prototype
		self.line_nb = line_nb
	
	def __repr__(self):
		return "Class " + self.name + ", line " + str(self.line_nb)

class ClassParser:	
	def parse(self, src):
		classes = []
		
		
		
		return classes


if __name__ == "__main__":
	parser = ClassParser()

	content = """/**
	 * This is a test class
	 * @param {String} test
	 */
	my.package.Class = function() {
		// This function does something
		var a = 1;

		/**
		 * some field
		 * @type {Boolean}
		 */
		this.someField = false; /* and some inline block comment */
	};

	my.package.Class.prototype = {
		/**
		 * Return the current value of the field
		 */
		getField : function() {
			// Just simply return the field
			var test = 1;
			for(var i = 0; i < 4; i++) {
				var something = test[i];
			}
			return this.someField; // And some inline comment
		}
	};
	
	var AnotherClass = function(){};
	AnotherClass.prototype.doSomething = function(a,b,c) {
		return a/b+c;
	};
	AnotherClass.prototype.doSomethingElse = function(foo, bar) {
		// Multiple stuff
		return foo * bar;
	};
	
	my.package.Class.prototype.setField = function(value) {
		this.value = value;
	}
	"""

	classes = parser.parse(content)

	assert len(classes) == 2, 1
	assert classes[0].name == "my.package.Class", 2
	assert classes[1].name == "AnotherClass", 3
	assert len(classes[0].prototype) == 2, 4
	assert len(classes[1].prototype) == 2, 5

	print "ALL TESTS OK"