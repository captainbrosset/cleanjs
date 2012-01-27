import re

from variableparser import VariableParser
from lineparser import LineParser

class FunctionData():
	"""Passed to each reviewer, as an element of the functions list, inside file_data.
	Instances of this class have the following attributes:
	- name: the name of the function
	- signature: an array of argument names
	- body: the text of the body of the function
	- variables: all variables declared in the function. Type parsers.variableparser.VariableData
	- has_return: whether the function has at least one return statement
	- lines: an instance of parsers.lineparser.LineParser.LineData"""
	
	def __init__(self, name, signature, body, lines, variables, has_return, line_nb):
		self.name = name
		self.signature = signature
		self.body = body
		self.lines = lines
		self.variables = variables
		self.line_nb = line_nb
		self.has_return = has_return
	
	def __repr__(self):
		return "Function " + self.name + ", line " + str(self.line_nb) + " (" + str(self.signature) + ") (" + str(len(self.lines.all_lines)) + " lines of code)"

class FunctionParser:

	FUNCTIONS_PATTERNS = ["function[\s]+([a-zA-Z0-9_$]+)[\s]*\(([a-zA-Z0-9,\s]*)\)[\s]*\{",
						"([a-zA-Z0-9_$]+)[\s]*=[\s]*function[\s]*\(([a-zA-Z0-9,\s]*)\)[\s]*\{",
						"([a-zA-Z0-9_$]+)[\s]*:[\s]*function[\s]*\(([a-zA-Z0-9,\s]*)\)[\s]*\{"]
	SIGNATURE_PATTERN = "[a-zA-Z0-9_$]+"
	FUNCTIONS_BODY_PROCESSOR_SEP = "[[FUNCTIONSTART]]"
	
	def _parse_signature(self, src):
		return re.findall(FunctionParser.SIGNATURE_PATTERN, src)
		
	def _parse_bodies(self, src, pattern):
		bodies = []

		while True:
			src = re.sub(pattern, FunctionParser.FUNCTIONS_BODY_PROCESSOR_SEP, src, 1)
			split = src.split(FunctionParser.FUNCTIONS_BODY_PROCESSOR_SEP, 1)
			if len(split) > 1:
				src = split[1]
				if src[0:1] == "\n":
					src = src[1:]
				if src[-1:] == "\n":
					src = src[:-1]
				
				# Read the chars from the beginning of this function to find the end
				opened_curly_brace = 0
				body = ""
				for char in src:
					# closing the function
					if char == "}" and opened_curly_brace == 0:
						break
					# closing an already opened brace
					if char == "}" and opened_curly_brace > 0:
						opened_curly_brace -= 1
					if char == "{":
						opened_curly_brace += 1
					body += char
				
				bodies.append(body)
			else:
				break

		return bodies
	
	def has_return_statement(self, code_lines):
		has_return = False
		for line in code_lines:
			if len(re.findall("[;\t\n \{\}]{1}return(?![a-zA-Z0-9_])|^return(?![a-zA-Z0-9_])", line.complete_line)) > 0:
				has_return = True
				break
		return has_return

	def parse(self, src):
		functions = []
		body_line_parser = LineParser()
		body_variable_parser = VariableParser()
		
		for pattern in FunctionParser.FUNCTIONS_PATTERNS:
			functions_bodies = self._parse_bodies(src, pattern)
			functions_signatures = re.finditer(pattern, src)
			for index, function_match in enumerate(functions_signatures):
				name = function_match.group(1)
				signature = self._parse_signature(function_match.group(2))
				body = functions_bodies[index]
				line_nb = src[0:function_match.start()].count("\n") + 1
				line_data = body_line_parser.parse(body, line_nb)
				variable_data = body_variable_parser.parse(body, line_nb)
				has_return = self.has_return_statement(line_data.get_code_lines())
				function = FunctionData(name, signature, body, line_data, variable_data, has_return, line_nb)
				functions.append(function)

		return functions


if __name__ == "__main__":
	parser = FunctionParser()

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

		var thisVariableReturnhasNameReturnreturn = 1;
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

	functions = parser.parse(content)

	assert len(functions) == 2, 1
	assert functions[0].name == "Class", 2
	assert len(functions[0].lines.all_lines) == 11, 3
	assert functions[1].name == "getField", 4
	assert len(functions[1].lines.all_lines) == 7, 5
	assert functions[0].has_return == False

	content_with_inner_function = """
	test = function() {
		var a = function() {
			var b = 1;
			return b;
		}

		if(test) {
			return false;
		}

		var i = 0;

		return a;
	};"""

	functions = parser.parse(content_with_inner_function)

	assert len(functions) == 2, 6
	assert functions[0].name == "test", 7
	assert len(functions[0].lines.all_lines) == 13, 8
	assert functions[1].name == "a", 9
	assert len(functions[1].lines.all_lines) == 3, 10
	assert len(functions[1].variables) == 1, 11
	assert functions[1].variables[0].line_nb == 4, 12
	assert functions[0].variables[2].name == "i", 13
	assert functions[0].variables[2].line_nb == 12, 14

	assert functions[1].lines.all_lines[1].line_number == 5, 15

	assert functions[0].has_return == True
	assert functions[1].has_return == True

	function_with_return = """
		getSomething = function() {
			if(test) return false;
		}

		getSomethingElse = function(){return a;}
		getSomethingElseYet = function(){
			return
		}
		wat = function() {var returnA = 0;}
	"""
	functions = parser.parse(function_with_return)
	assert functions[0].has_return == True
	assert functions[1].has_return == True
	assert functions[2].has_return == True
	assert functions[3].has_return == False

	print "ALL TESTS OK"