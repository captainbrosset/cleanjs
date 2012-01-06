from basedata import BaseData

class FunctionData(BaseData):
	"""Passed to each reviewer, as an element of the functions list, inside file_data.
	Instances of this class have the following attributes:
	- name: the name of the function
	- signature: an array of argument names
	- body: the text of the body of the function
	- line_data: an instance of utils.parsers.lineparser.LineParser.LineData"""
	def __init__(self, name, signature, body, line_data, line_nb):
		self.name = name
		self.signature = signature
		self.body = body
		self.line_data = line_data
		self.line_nb = line_nb
	def find_line_numbers(self, pattern, flags=None):
		"""Given a re pattern, return an array of line numbers where it is found in the function"""
		return self.find_line_numbers_in_content(self.body, pattern, flags)
	def __repr__(self):
		return "[line " + self.line_nb + "] " + self.name + "(" + str(self.signature) + "){" + self.body + "}"