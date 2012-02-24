import re

from variableparser import VariableParser, VariableData
from lineparser import LineParser
import visitor

class FunctionData(visitor.Entity):
	"""Passed to each reviewer, as an element of the functions list, inside file_data.
	Instances of this class have the following attributes:
	- name: the name of the function
	- signature: an array of argument names
	- body: the text of the body of the function
	- variables: all variables declared in the function. Type parsers.variableparser.VariableData
	- nb_return: number of return statement in the function
	- lines: an instance of parsers.lineparser.FileLines
	- complexity: an integer showing the cyclomatic complexity of the function (minimum 1)
	- identifiers_usage: meant to be used through the get_identifier_usage(name) function to know where a given name is used in the function"""
	
	def __init__(self, name, body, line_number, signature, start_pos, end_pos, variables, nb_return):
		super(FunctionData, self).__init__(line_number, start_pos, end_pos)

		self.name = name
		self.body = body
		self.signature = signature

		self.lines = None
		self.variables = variables
		self.nb_return = nb_return

		self.complexity = 1

		self.identifiers_usage = {}
	
	def has_variable(self, name):
		for var in self.variables:
			if var.name == name:
				return True
		return False

	def ensure_identifier_usage_exists(self, name):
		if not self.identifiers_usage.has_key(name):
			self.identifiers_usage[name] = []

	def increment_identifiers_usage(self, name, line_number):
		self.ensure_identifier_usage_exists(name)
		self.identifiers_usage[name].append(line_number)

	def get_identifier_usage(self, name):
		self.ensure_identifier_usage_exists(name)
		return self.identifiers_usage[name]

	def __repr__(self):
		return "Function " + self.name + ", line " + str(self.line_number) + " (" + str(self.signature) + ")"


class FunctionBody(object):
	def __init__(self, source, start_pos, end_pos):
		self.outer_body = source[start_pos:end_pos]
		self.inner_body = self.extract_inner_body()
		self.start_pos = self.get_inner_start_pos(start_pos)
		self.end_pos = self.get_inner_end_pos(end_pos)

	def extract_inner_body(self):
		return self.outer_body[self.outer_body.find("{")+1:self.outer_body.rfind("}")]
	
	def get_inner_start_pos(self, start_pos):
		return start_pos + self.outer_body.find("{") + 1

	def get_inner_end_pos(self, end_pos):
		return end_pos - 1


class FunctionParser(object):
	"""
	Parser/visitor for functions
	"""

	def __init__(self):
		self.functions = []

	def add_function(self, name, line_number, signature, start_pos, end_pos, source):
		body = FunctionBody(source, start_pos, end_pos)

		function = FunctionData(name, body.inner_body, line_number, signature, body.start_pos, body.end_pos, [], 0)
		self.functions.append(function)

	def add_var(self, function, name, is_nodejs_require, line_number, start, end):
		is_already_there = False
		for var in function.variables:
			if var.name == name and var.line_number == line_number:
				is_already_there = True
		
		if not is_already_there:
			function.variables.append(VariableData(name, is_nodejs_require, line_number, start, end))

	def get_functions_nesting(self, position):
		"""Given a position, return the list of function(s) this position is nested into.
		The list returned is ordered by deepest function first"""
		functions = []
		for function in self.functions:
			if function.end_pos > position and function.start_pos < position:
				functions.append(function)
		return sorted(functions, key=lambda f: -f.start_pos)

	def increase_function_complexity(self, node):
		functions = self.get_functions_nesting(node.start)
		if len(functions) > 0:
			functions[0].complexity += 1

	def visit_IF(self, node, source): self.increase_function_complexity(node)
	def visit_AND(self, node, source): self.increase_function_complexity(node)
	def visit_OR(self, node, source): self.increase_function_complexity(node)
	def visit_FOR(self, node, source): self.increase_function_complexity(node)
	def visit_WHILE(self, node, source): self.increase_function_complexity(node)
	def visit_TRY(self, node, source): self.increase_function_complexity(node)
	def visit_CATCH(self, node, source): self.increase_function_complexity(node)
	def visit_SWITCH(self, node, source): self.increase_function_complexity(node)
	def visit_CASE(self, node, source): self.increase_function_complexity(node)

	def visit_VAR(self, node, source):
		functions = self.get_functions_nesting(node.start)
		if len(functions) > 0:
			variable_parser = VariableParser()
			variables = variable_parser.extract_variables(node)
			for variable in variables:
				self.add_var(functions[0], variable["name"], variable["is_nodejs_require"], variable["line_number"], variable["start_pos"], variable["end_pos"])

	def visit_RETURN(self, node, source):
		functions = self.get_functions_nesting(node.start)
		if len(functions) > 0:
			functions[0].nb_return += 1

	def visit_FUNCTION(self, node, source):
		# Named functions only, the getattr returns None if name doesn't exist
		if node.type == "FUNCTION" and getattr(node, "name", None):
			self.add_function(node.name, node.lineno, node.params, node.start, node.end, source)

	def visit_IDENTIFIER(self, node, source):
		# Anonymous functions declared with var name = function() {};
		try:
			if node.type == "IDENTIFIER" and hasattr(node, "initializer") and node.initializer.type == "FUNCTION":
				self.add_function(node.name, node.lineno, node.initializer.params, node.start, node.initializer.end, source)
		except Exception as e:
			pass
		
		functions = self.get_functions_nesting(node.start)
		if len(functions) > 0:
			for function in functions:
				function.increment_identifiers_usage(node.value, node.lineno)
				if function.has_variable(node.value):
					break

	def visit_ASSIGN(self, node, source):
		if node[1].type == "FUNCTION":
			self.add_function(node[0].value, node[1].lineno, node[1].params, node[1].start, node[1].end, source)

	def visit_PROPERTY_INIT(self, node, source):
		# Anonymous functions declared as a property of an object
		try:
			if node.type == "PROPERTY_INIT" and node[1].type == "FUNCTION":
				self.add_function(node[0].value, node[0].lineno, node[1].params, node[1].start, node[1].end, source)
		except Exception as e:
			pass


if __name__ == "__main__":

	# Testing that the function body inner code extractor works

	function_code = """function test() {
		var a = 1;
		a += 1;
		return a;
	}"""
	whole_code = "var w = window;" + function_code + "test(w);"
	body = FunctionBody(whole_code, 15, 15 + len(function_code))
	assert body.outer_body == function_code
	assert body.inner_body == """
		var a = 1;
		a += 1;
		return a;
	"""
	assert body.start_pos == 32
	assert body.end_pos == 69

	# Testing that functions nested within each other are reported correctly

	parser = FunctionParser()
	parser.add_function("function1", 1, [], 1, 50, "")
	parser.add_function("nestedInFunction1", 3, [], 10, 30, "")
	parser.add_function("function2", 5, [], 60, 100, "")
	parser.add_function("nestedInFunction2", 7, [], 80, 90, "")
	parser.add_function("nestedInNestedFunction2", 9, [], 85, 89, "")
	nesting = parser.get_functions_nesting(86)
	assert len(nesting) == 3
	assert nesting[0].name == "nestedInNestedFunction2"
	assert nesting[1].name == "nestedInFunction2"
	assert nesting[2].name == "function2"

	# Testing that identifiers used in functions are reported in the right functions
	# Including parent functions in case identifier is global and is defined in parent function

	class Mock:
		__init__ = lambda self, **kw: setattr(self, '__dict__', kw)

	parser = FunctionParser()
	parser.add_function("rootFunction", 1, [], 1, 70, "")
	parser.add_function("parentFunction", 1, [], 2, 50, "")
	parser.add_var(parser.functions[1], "variableDefinedInParentFunction", False, 3, 5, 6)
	parser.add_function("childFunction", 3, [], 10, 30, "")
	parser.add_var(parser.functions[2], "variableDefinedInChildFunction", False, 3, 12, 15)

	identifier = Mock(type="IDENTIFIER", value="variableDefinedInParentFunction", lineno=4, start=20, end=22)
	parser.visit_IDENTIFIER(identifier, "")

	assert len(parser.functions) == 3
	assert len(parser.functions[0].variables) == 0
	assert len(parser.functions[1].variables) == 1
	assert parser.functions[1].variables[0].name == "variableDefinedInParentFunction"
	assert len(parser.functions[2].variables) == 1
	assert parser.functions[2].variables[0].name == "variableDefinedInChildFunction"

	assert parser.functions[2].identifiers_usage.has_key("variableDefinedInParentFunction")
	assert parser.functions[1].identifiers_usage.has_key("variableDefinedInParentFunction"), "Variable is used in nested function but defined in parent, should be reported as used in parent"

	print "ALL TESTS OK"