import re

from data.functiondata import FunctionData
from data.variabledata import VariableData
from parsers.lineparser import LineParser

class FileInfoParser():
	
	FUNCTIONS_PATTERNS = ["function[\s]+([a-zA-Z0-9_$]+)[\s]*\(([a-zA-Z0-9,\s]*)\)[\s]*\{",
						"([a-zA-Z0-9_$]+)[\s]*=[\s]*function[\s]*\(([a-zA-Z0-9,\s]*)\)[\s]*\{",
						"([a-zA-Z0-9_$]+)[\s]*:[\s]*function[\s]*\(([a-zA-Z0-9,\s]*)\)[\s]*\{"]
	SIGNATURE_PATTERN = "[a-zA-Z0-9_$]+"
	FUNCTIONS_BODY_PROCESSOR_SEP = "[[FUNCTIONSTART]]"
	VARIABLES_PATTERN = "var[\s]+([a-zA-Z0-9_$]+)"
		
	def _parse_signature(self, src):
		return re.findall(FileInfoParser.SIGNATURE_PATTERN, src)
	
	def _parse_bodies(self, src, pattern):
		# FIXME: the parser fails to understand nested functions (a function inside another function)
		bodies = []
		processed_src = re.sub(pattern, FileInfoParser.FUNCTIONS_BODY_PROCESSOR_SEP, src)
		src_split_by_first_occurence = processed_src.split(FileInfoParser.FUNCTIONS_BODY_PROCESSOR_SEP, 1)
		
		if len(src_split_by_first_occurence) > 1:
			processed_src = src_split_by_first_occurence[1]
			unprocessed_bodies = processed_src.split(FileInfoParser.FUNCTIONS_BODY_PROCESSOR_SEP)
		
			for body in unprocessed_bodies:
				opened_curly_brace = 0
				content = ""
				for char in body:
					# closing the function
					if char == "}" and opened_curly_brace == 0:
						break
					# closing an already opened brace
					if char == "}" and opened_curly_brace > 0:
						opened_curly_brace -= 1
					if char == "{":
						opened_curly_brace += 1
					content += char
				bodies.append(content)
		
		return bodies
		
	def parse_functions(self, src):
		functions = []
		body_line_parser = LineParser()
		
		for pattern in FileInfoParser.FUNCTIONS_PATTERNS:
			functions_bodies = self._parse_bodies(src, pattern)
			functions_signatures = re.finditer(pattern, src)
			for index, function_match in enumerate(functions_signatures):
				name = function_match.group(1)
				signature = self._parse_signature(function_match.group(2))
				body = functions_bodies[index]
				line_nb = src[0:function_match.start()].count("\n") + 1
				line_data = body_line_parser.parse(body)
				function = FunctionData(name, signature, body, line_data, line_nb)
				functions.append(function)

		return functions
	
	def parse_variables(self, src):
		matches = re.finditer(FileInfoParser.VARIABLES_PATTERN, src)
		variables = []
		for match in matches:
			variable = VariableData(match.group(1), src[0:match.start()].count("\n") + 1)
			variables.append(variable)
		return variables
	
	def parse_lines(self, src):
		return LineParser().parse(src)

if __name__ == "__main__":
	parser = FileInfoParser()
	
	content = """/**
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
	
	variables = parser.parse_variables(content)
	
	assert len(variables) == 4, 1
	assert variables[0] == "a", 2
	assert variables[1] == "test", 3
	assert variables[2] == "i", 4
	assert variables[3] == "something", 5
	
	print "ALL TESTS OK"