from basedata import BaseData

class FunctionData(BaseData):
	"""Passed to each reviewer, as an element of the functions list, inside file_data"""
	def __init__(self, name = "anonymous", signature = [], body = "", line_nb = None):
		self.name = name
		self.signature = signature
		self.body = body
		self.line_nb = line_nb
	def find_line_numbers(self, pattern, flags=None):
		"""Given a re pattern, return an array of line numbers where it is found in the function"""
		return self.find_line_numbers_in_content(self.body, pattern, flags)
	def __repr__(self):
		return "[line " + self.line_nb + "] " + self.name + "(" + str(self.signature) + "){" + self.body + "}"