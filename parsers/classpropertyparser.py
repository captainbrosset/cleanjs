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
		self.initialized = False
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
		prop = self.get_property(name)
		if not prop:
			prop = ClassPropertyData(name, line_number, start, end)
			self.properties.append(prop)
		return prop

	def visit_DOT(self, node, source):
		if node[0].type == "THIS":
			prop = self.add_property(node[1].value, node[1].lineno, node[1].start, node[1].end)
			prop.usage += 1

	def visit_ASSIGN(self, node, source):
		if node[0].type == "DOT" and node[0][0].value == "this":
			prop = self.add_property(node[0].value, node[0].lineno, node[0].start, node[0].end)
			prop.initialized = True

if __name__ == "__main__":
	print "NO TESTS TO RUN"