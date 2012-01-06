class VariableData:
	"""Passed to each reviewer, as an element of the variables list, inside file_data.
	Instances of this class have the following attributes:
	- name: the name of the variable
	- line_nb: the line number in the file where the variable occurs"""
	def __init__(self, name, line_nb):
		self.name = name
		self.line_nb = line_nb