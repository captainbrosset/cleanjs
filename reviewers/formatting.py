import re

class Reviewer():
	def get_name(self):
		return "formatting"
		
	def get_help(self):
		return """Uniform code formatting across files and across members of a team is key to maintainability.
		This reviewer checks:
		- if the file is correctly formated (based on whitespace positions in function declaration as well as in other statements)
		- if the file contains several empty lines in a row"""
	
	def review_statement_spacing(self, file_content, message_bag):
		bad_format = len(re.findall("[a-zA-Z0-9_$]+: function", file_content))
		bad_format += len(re.findall("[a-zA-Z0-9_$]+:function", file_content))
		bad_format += len(re.findall(":function\(", file_content))
		bad_format += len(re.findall(": function\(", file_content))
		bad_format += len(re.findall(":function \(", file_content))
		bad_format += len(re.findall("if\(", file_content))
		bad_format += len(re.findall("\)\{", file_content))
		
		if bad_format != 0:
			message_bag.add_error(self, "It seems you haven't properly formatted your file. Make sure you have configured a proper formatter")
	
	def review_empty_lines(self, file_data, message_bag):
		matches = file_data.find_line_numbers("\n[\s]*\n[\s]*\n")
		for match in matches:
			message_bag.add_warning(self, "There are several empty lines in a row, either you didn't format the file correctly, or you are trying to space complex things out.", match.line_number)
	
	def review(self, file_data, message_bag):
		self.review_statement_spacing(file_data.content, message_bag)
		self.review_empty_lines(file_data, message_bag)