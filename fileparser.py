import re

from parsers.lineparser import LineParser
from parsers.functionparser import FunctionParser
from parsers.variableparser import VariableParser

def get_file_data_from_content(src_file_name, src_file_content):
	"""Use this to gather data for file, given its content"""
	src_file_functions = FunctionParser().parse(src_file_content)
	src_file_variables = VariableParser().parse(src_file_content)
	src_file_lines = LineParser().parse(src_file_content)

	return FileData(src_file_name, src_file_content, src_file_lines, src_file_functions, src_file_variables)

def get_file_data_from_file(src_file_name):
	"""Use this to gather data for file, given its path and name"""
	return get_file_data_from_content(src_file_name, open(src_file_name, 'r').read())

class FileData():
	"""An instance of this class is passed to reviewers, in their review function.
	This class holds the different information about the file being reviewed.
	Instances of this class have the following attributes:
	- name: the name of the file
	- content: the whole text content of the file
	- lines: an instance of utils.parsers.lineparser.LineData
	- functions: an array of instances of utils.parsers.functionparser.FunctionData
	- variables: an array of instances of utils.parsers.variableparser.VariableData"""

	def __init__(self, name, content, lines, functions, variables):
		self.name = name
		self.content = content
		self.lines = lines
		self.functions = functions
		self.variables = variables

	def __repr__(self):
		report = "file " + self.name + " (" + str(len(self.lines.total_lines)) + " lines of code)"
		for function in self.functions:
			report += function.toString()
		return report

	def find_line_numbers(self, pattern, flags=None):
		"""Given a re pattern, find all lines where it occurs in the file source and 
		return an array of LineNumberMatchObject objects."""
		results = []

		# FIXME: Seems I can't pass flags=None to the finditer function. Find a way to make this better.
		if flags:
			matches = re.finditer(pattern, self.content, flags=flags)
		else:
			matches = re.finditer(pattern, self.content)

		for match in matches:
			result = LineNumberMatchObject(self.content[0:match.start()].count("\n") + 1, match)
			results.append(result)

		return results

class LineNumberMatchObject:
	def __init__(self, line_number, match_object):
		self.line_number = line_number
		self.match_object = match_object