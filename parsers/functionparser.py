import re

from variableparser import VariableParser
from lineparser import LineParser
import visitor

class FunctionData(visitor.Entity):
	"""Passed to each reviewer, as an element of the functions list, inside file_data.
	Instances of this class have the following attributes:
	- name: the name of the function
	- signature: an array of argument names
	- body: the text of the body of the function
	- variables: all variables declared in the function. Type parsers.variableparser.VariableData
	- has_return: whether the function has at least one return statement
	- lines: an instance of parsers.lineparser.LineParser.LineData"""
	
	def __init__(self, name, body, line_number, signature, start_pos, end_pos, lines, variables, has_return):
		super(Function, self).__init__(line_number, start_pos, end_pos)
		
		self.name = name
		self.body = body
		self.signature = signature

		self.lines = lines
		self.variables = variables
		self.has_return = has_return
	
	def __repr__(self):
		return "Function " + self.name + ", line " + str(self.line_number) + " (" + str(self.signature) + ") (" + str(len(self.lines.all_lines)) + " lines of code)"

class FunctionParser:	
	def __init__(self):
		self.entities = []
	
	def add_function(self, name, body, line_number, signature, start_pos, end_pos, source):
		parsed_lines = LineParser().parse(body)
		parsed_vars = VariableParser().parse(body)
		has_return = self.has_return_statement(parsed_lines.get_code_lines())
		function = Function(name, body, line_number, signature, start_pos, end_pos, parsed_lines, parsed_vars, has_return)
		self.entities.append(function)

	def has_return_statement(self, code_lines):
		has_return = False
		for line in code_lines:
			if len(re.findall("[;\t\n \{\}]{1}return(?![a-zA-Z0-9_])|^return(?![a-zA-Z0-9_])", line.complete_line)) > 0:
				has_return = True
				break
		return has_return

	def visit_FUNCTION(self, node, source):
		# Named functions only, the getattr returns None if name doesn't exist
		if node.type == "FUNCTION" and getattr(node, "name", None):
			self.add_function(node.name, source[node.start:node.end], node.lineno, node.params, node.start, node.end, source)

	def visit_IDENTIFIER(self, node, source):
		# Anonymous functions declared with var name = function() {};
		try:
			if node.type == "IDENTIFIER" and hasattr(node, "initializer") and node.initializer.type == "FUNCTION":
				self.add_function(node.name, source[node.start:node.initializer.end], node.lineno, node.initializer.params, node.start, node.initializer.end, source)
		except Exception as e:
			pass

	def visit_ASSIGN(self, node, source):
		if node[1].type == "FUNCTION":
			self.add_function(node[0].value, source[node[1].start:node[1].end], node[1].lineno, node[1].params, node[1].start, node[1].end, source)

	def visit_PROPERTY_INIT(self, node, source):
		# Anonymous functions declared as a property of an object
		try:
			if node.type == "PROPERTY_INIT" and node[1].type == "FUNCTION":
				self.add_function(node[0].value, source[node.start:node[1].end], node[0].lineno, node[1].params, node.start, node[1].end, source)
		except Exception as e:
			pass


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

	# FIXME: this unit test is failing and shows why a true Js parser is far better compared to the simple regexp used so far
	comment_block_with_function = """
	/**
	 * This is the comment of a function
	 * you can use it like this:
	 * addSubcribe({
	 * 	fn: function() {
	 * 		// this is a test
	 * 	}
	 * });
	 */
	 addSubcribe = function() {
	 	
	 }
	"""
	functions = parser.parse(comment_block_with_function)
	assert len(functions) == 1, "Incorrect number of functions parsed in the code"
	assert functions[0].name == "addSubscribe"

	print "ALL TESTS OK"