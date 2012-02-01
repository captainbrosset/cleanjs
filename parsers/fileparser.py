import re

from jsparser import JSFileParser
from lineparser import LineParser
from functionparser import FunctionParser
from variableparser import VariableParser

class FileData():
	"""An instance of this class is passed to reviewers, in their review function.
	This class holds the different information about the file being reviewed.
	Instances of this class have the following attributes:
	- name: the name of the file
	- content: the whole text content of the file
	- lines: an instance of utils.parsers.lineparser.LinesData
	- functions: an array of instances of utils.parsers.functionparser.FunctionData
	- variables: an array of instances of utils.parsers.variableparser.VariableData"""

	def __init__(self, name, content, lines, functions, variables):
		self.name = name
		self.content = content
		self.lines = lines
		self.functions = functions
		self.variables = variables

	def __repr__(self):
		report = "file " + self.name + " (" + str(len(self.lines.all_lines)) + " lines of code)"
		for function in self.functions:
			report += function.toString()
		return report

def get_file_data_from_content(src_file_name, src_file_content):
	"""Use this to gather data for file, given its content.
	Will raise a jsparser.ParsingError if the syntax is incorrect"""

	parser = JSFileParser(src_file_content)

	function_parser = FunctionParser()
	parser.add_visitor(function_parser)

	variable_parser = VariableParser()
	parser.add_visitor(variable_parser)

	line_parser = LineParser()
	parser.add_visitor(line_parser)
	
	parser.parse()
	
	src_file_functions = function_parser.functions
	src_file_variables = variable_parser.variables
	src_file_lines = line_parser.lines_data

	return FileData(src_file_name, src_file_content, src_file_lines, src_file_functions, src_file_variables)

def get_file_data_from_file(src_file_name):
	"""Use this to gather data for file, given its path and name.
	Will raise a jsparser.ParsingError if the syntax is incorrect"""

	return get_file_data_from_content(src_file_name, open(src_file_name, 'r').read())


if __name__ == "__main__":
	content = """
	/**
	 * This is a test class
	 * @param {String} test
	 */
	my.package.Class = function() {
		// This function does something
		var a = 1;

		/**
		 * some field
		 * @type {Boolean}
		 */
		this.someField = false; /* and some inline block comment */
	};

	my.package.Class.prototype = {
		/**
		 * Return the current value of the field
		 */
		getField : function() {
			// Just simply return the field
			var test = 1;
			for(var i = 0; i < 4; i++) {
				var something = test[i];
			}
			return this.someField; // And some inline comment
		}
	};
	"""
	name = "test"
	file_data = get_file_data_from_content(name, content)

	assert file_data.name == name
	assert file_data.content == content
	assert len(file_data.lines.all_lines) == 30
	assert len(file_data.functions) == 2
	assert len(file_data.variables) == 4

	print "ALL TESTS OK"