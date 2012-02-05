import re

import visitor

class VariableData(visitor.Entity):
	"""Passed to each reviewer, as an element of the variables list, inside file_data.
	Instances of this class have the following attributes:
	- name: the name of the variable
	- line_number: the line number in the file where the variable occurs"""
	
	def __init__(self, name, line_number, start_pos, end_pos):
		super(VariableData, self).__init__(line_number, start_pos, end_pos)
		self.name = name
	
	def __repr__(self):
		return "Variable " + self.name + "(line " + str(self.line_number) + ")"

class VariableParser:
	def __init__(self):
		self.variables = []
	
	def add_var(self, name, line_number, start, end):
		is_already_there = False
		for var in self.variables:
			if var.name == name and var.line_number == line_number:
				is_already_there = True
		
		if not is_already_there:
			self.variables.append(VariableData(name, line_number, start, end))

	def visit_VAR(self, node, source):
		for subvar_node in node:
			if getattr(subvar_node, "initializer", False):
				self.add_var(subvar_node.value, subvar_node.lineno, subvar_node.start, subvar_node.initializer.end)
			else:
				self.add_var(subvar_node.value, subvar_node.lineno, subvar_node.start, subvar_node.end)


if __name__ == "__main__":
	print "NO TESTS TO RUN"