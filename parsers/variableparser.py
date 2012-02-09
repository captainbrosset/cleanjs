import re

import visitor

class VariableData(visitor.Entity):
	"""Passed to each reviewer, as an element of the variables list, inside file_data.
	Instances of this class have the following attributes:
	- name: the name of the variable
	- is_nodejs_require: was the variable initialized as a nodejs required dependency
	- line_number: the line number in the file where the variable occurs"""
	
	def __init__(self, name, is_nodejs_require, line_number, start_pos, end_pos):
		super(VariableData, self).__init__(line_number, start_pos, end_pos)
		self.name = name
		self.is_nodejs_require = is_nodejs_require
	
	def __repr__(self):
		return "Variable " + self.name + " (line " + str(self.line_number) + ")"

class VariableParser:
	def __init__(self):
		self.variables = []
	
	def add_var(self, name, is_nodejs_require, line_number, start, end):
		is_already_there = False
		for var in self.variables:
			if var.name == name and var.line_number == line_number:
				is_already_there = True
		
		if not is_already_there:
			self.variables.append(VariableData(name, is_nodejs_require, line_number, start, end))

	def is_initializer_call_to_require(self, initializer):
		return initializer.type == "CALL" and initializer[0].value == "require"

	def is_var_being_initialized(self, node):
		return getattr(node, "initializer", False)

	def is_string_value(self, node, value):
		return node.type == "STRING" and node.value == value

	def is_nodejs_require_var_init(self, initializer, var_name):
		is_nodejs_require = False
		if self.is_initializer_call_to_require(initializer):
			if self.is_string_value(initializer[1][0], var_name):
				is_nodejs_require = True
		return is_nodejs_require

	def extract_variables(self, node):
		variables = []
		for subvar_node in node:
			if self.is_var_being_initialized(subvar_node):
				is_nodejs_require = self.is_nodejs_require_var_init(subvar_node.initializer, subvar_node.value)
				variables.append({
					"name": subvar_node.value,
					"is_nodejs_require": is_nodejs_require,
					"line_number": subvar_node.lineno,
					"start_pos": subvar_node.start,
					"end_pos": subvar_node.initializer.end
				})
			else:
				variables.append({
					"name": subvar_node.value,
					"is_nodejs_require": False,
					"line_number": subvar_node.lineno,
					"start_pos": subvar_node.start,
					"end_pos": subvar_node.end
				})
		return variables

	def visit_VAR(self, node, source):
		variables = self.extract_variables(node)
		for variable in variables:
			self.add_var(variable["name"], variable["is_nodejs_require"], variable["line_number"], variable["start_pos"], variable["end_pos"])

if __name__ == "__main__":
	print "NO TESTS TO RUN"