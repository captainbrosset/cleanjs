import re

class FileData():
	"""A FileData instance is passed to reviewers"""
	def __init__(self, name, content, lines, functions, variables):
		self.name = name
		self.content = content
		self.lines = lines
		self.functions = functions
		self.variables = variables
	def find_line_numbers(self, pattern, flags=None):
		"""Given a re pattern, return an array of line numbers where it is found in the whole file
		If you are looking to restrict this to a particular function, see the same method on the function object instead"""
		line_numbers = []
		# FIXME: make this better
		if flags:
			matches = re.finditer(pattern, self.content, flags=flags)
		else:
			matches = re.finditer(pattern, self.content)
		for match in matches:
			line_numbers.append(self.content[0:match.start()].count("\n") + 1)
		return line_numbers
	def __repr__(self):
		return "[file " + self.name + "]"