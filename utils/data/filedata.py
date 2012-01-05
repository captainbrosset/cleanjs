from basedata import BaseData

class FileData(BaseData):
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
		return self.find_line_numbers_in_content(self.content, pattern, flags)
	def __repr__(self):
		return "[file " + self.name + "]"