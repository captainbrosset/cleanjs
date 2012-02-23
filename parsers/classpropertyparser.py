import re

import visitor

class ClassPropertyData(visitor.Entity):
	"""Passed to each reviewer, as an element of the this list, inside file_data.
	Instances of this class have the following attributes:
	- name: the name of the class property (this.theName)
	- line_number: the line number in the file where the property occurs"""
	
	def __init__(self, name, line_number, start_pos, end_pos):
		super(ClassPropertyData, self).__init__(line_number, start_pos, end_pos)
		self.name = name
		self.usage = -1;
	
	def __repr__(self):
		return "Class property " + self.name + "(line " + str(self.line_number) + ")"

class ClassPropertyParser(object):
	def __init__(self):
		self.properties = []

	def get_property(self, name):
		for prop in self.properties:
			if prop.name == name:
				return prop
		return None
	
	def add_property(self, name, line_number, start, end):
		is_already_there = False
		for property in self.properties:
			if property.name == name and property.line_number == line_number:
				is_already_there = True
		
		if not is_already_there:
			self.properties.append(ClassPropertyData(name, line_number, start, end))

	def visit_DOT(self, node, source):
		if node[0].type == "THIS":
			prop = self.get_property(node[1].value)
			if prop:
				prop.usage += 1

	def visit_ASSIGN(self, node, source):
		if node[0].type == "DOT" and node[0][0].value == "this":
			property_name = node[0].value
			self.add_property(property_name, node[0].lineno, node[0].start, node[0].end)

if __name__ == "__main__":
	print "NO TESTS TO RUN"