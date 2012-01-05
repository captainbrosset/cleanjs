import re

class FunctionData():
	"""Passed to each reviewer, as an element of the functions list, inside file_data"""
	def __init__(self, name = "anonymous", signature = [], body = "", line_nb = None):
		self.name = name
		self.signature = signature
		self.body = body
		self.line_nb = line_nb
	def find_line_numbers(self, pattern, flags):
		"""Given a re pattern, return an array of line numbers where it is found in the function"""
		line_numbers = []
		matches = re.finditer(pattern, self.body, flags=flags)
		for match in matches:
			line_numbers.append(self.body[0:match.start()].count("\n") + 1)
		return line_numbers
	def __repr__(self):
		return "[line " + self.line_nb + "] " + self.name + "(" + str(self.signature) + "){" + self.body + "}"