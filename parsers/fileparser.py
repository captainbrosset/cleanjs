import re

from lineparser import LineParser
from functionparser import FunctionParser
from variableparser import VariableParser

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


if __name__ == "__main__":	
	print "NO TESTS TO RUN"