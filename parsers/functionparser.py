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
	- has_return: whether the function has at least one return statement
	- lines: an instance of parsers.lineparser.LineParser.LineData"""
	
	def __init__(self, name, body, line_number, signature, start_pos, end_pos, variables, has_return):
		super(FunctionData, self).__init__(line_number, start_pos, end_pos)

		self.name = name
		self.body = body
		self.signature = signature

		self.lines = None
		self.variables = variables
		self.has_return = has_return
	
	def __repr__(self):
		return "Function " + self.name + ", line " + str(self.line_number) + " (" + str(self.signature) + ") (" + str(len(self.lines.all_lines)) + " lines of code)"


class FunctionParser:	
	def __init__(self):
		self.functions = []
		self.last_function = None

	def add_function(self, name, body, line_number, signature, start_pos, end_pos, source):
		inner_body_start_pos = start_pos + body.find("{") + 1
		inner_body_end_pos = end_pos - 1
		inner_body = body[body.find("{")+1:body.rfind("}")]

		function = FunctionData(name, inner_body, line_number, signature, inner_body_start_pos, inner_body_end_pos, [], False)
		self.functions.append(function)

	def add_var(self, function, name, line_number, start, end):
		is_already_there = False
		for var in function.variables:
			if var.name == name and var.line_number == line_number:
				is_already_there = True
		
		if not is_already_there:
			function.variables.append(VariableData(name, line_number, start, end))

	def get_last_function(self):
		if len(self.functions) > 0:
			return self.functions[len(self.functions) - 1]
		else:
			return None

	def is_in_function(self, start_pos):
		last_function = self.get_last_function()
		return last_function and last_function.end_pos > start_pos

	def visit_VAR(self, node, source):
		if self.is_in_function(node.start):
			if getattr(node[0], "initializer", False):
				self.add_var(self.get_last_function(), node[0].value, node.lineno, node.start, node[0].initializer.end)
			else:
				self.add_var(self.get_last_function(), node[0].value, node.lineno, node.start, node.end)

	def visit_RETURN(self, node, source):
		if self.is_in_function(node.start):
			self.get_last_function().has_return = True

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
	print "NO TESTS TO RUN"