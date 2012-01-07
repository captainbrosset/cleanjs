import re

class VariableData:
	"""Passed to each reviewer, as an element of the variables list, inside file_data.
	Instances of this class have the following attributes:
	- name: the name of the variable
	- line_nb: the line number in the file where the variable occurs"""
	def __init__(self, name, line_nb):
		self.name = name
		self.line_nb = line_nb

class VariableParser():
	
	VARIABLES_PATTERN = "var[\s]+([a-zA-Z0-9_$]+)"
	
	def parse(self, src):
		matches = re.finditer(VariableParser.VARIABLES_PATTERN, src)
		variables = []
		for match in matches:
			variable = VariableData(match.group(1), src[0:match.start()].count("\n") + 1)
			variables.append(variable)
		return variables


if __name__ == "__main__":
	parser = VariableParser()

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
	"""
	variables = parser.parse(content)

	assert len(variables) == 4, 1
	assert variables[0].name == "a", 2
	assert variables[1].name == "test", 3
	assert variables[2].name == "i", 4
	assert variables[3].name == "something", 5
	
	print "ALL TESTS OK"