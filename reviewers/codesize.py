import re

from helpers import variablelength
from helpers import wordmeaning

class Reviewer():
	WARN_MAX_FILE_LINE_NUMBER = 150
	ERROR_MAX_FILE_LINE_NUMBER = 300
	WARN_MAX_FUNCTION_LINE_NUMBER = 20
	ERROR_MAX_FUNCTION_LINE_NUMBER = 50
	WARN_MIN_NAME_SIZE = 3
	ERROR_MIN_NAME_SIZE = 2
	WARN_MAX_NAME_SIZE = 35
	ERROR_MAX_NAME_SIZE = 50
	WARN_MAX_ARGUMENT_NB = 5
	ERROR_MAX_ARGUMENT_NB = 10
	ERROR_MAX_LINE_LENGTH = 120

	def __init__(self, config_reader=None):
		self.config_reader = config_reader

	def get_name(self):
		return "code size"

	def is_line_too_long(self, line):
		if line[-1:] == "\n":
			line = line[0:-1]
		return len(line) > Reviewer.ERROR_MAX_LINE_LENGTH

	def review_line_length(self, lines, message_bag):
		for line in lines:
			if self.is_line_too_long(line.complete_line):
				message_string = self.config_reader.get("codesize", "line_too_long", Reviewer.ERROR_MAX_LINE_LENGTH, len(line.complete_line))
				message_bag.add_warning(self, message_string, line.line_number)

	def review_nb_of_arguments(self, functions, message_bag):
		for function in functions:
			if len(function.signature) > Reviewer.ERROR_MAX_ARGUMENT_NB:
				message_string = self.config_reader.get("codesize", "too_many_function_arguments_error", Reviewer.ERROR_MAX_ARGUMENT_NB, function.name, len(function.signature))
				message_bag.add_error(self, message_string, function.line_number)
			elif len(function.signature) > Reviewer.WARN_MAX_ARGUMENT_NB:
				message_string = self.config_reader.get("codesize", "too_many_function_arguments_warning", Reviewer.WARN_MAX_ARGUMENT_NB, function.name, len(function.signature))
				message_bag.add_warning(self, message_string, function.line_number)
	
	def review_line_number_in_file(self, lines, message_bag):
		# FIXME: comment lines are NOT ignored, should be?!
		nb = len(lines.all_lines)
		if nb > Reviewer.ERROR_MAX_FILE_LINE_NUMBER:
			message_string = self.config_reader.get("codesize", "too_many_lines_in_file_error", Reviewer.ERROR_MAX_FILE_LINE_NUMBER, nb)
			message_bag.add_error(self, message_string, 1)
		elif nb > Reviewer.WARN_MAX_FILE_LINE_NUMBER:
			message_string = self.config_reader.get("codesize", "too_many_lines_in_file_warning", Reviewer.WARN_MAX_FILE_LINE_NUMBER, nb)
			message_bag.add_warning(self, message_string, 1)

	def is_function_empty(self, function):
		return function.body.strip() == ""

	def review_line_number_in_functions(self, file_functions, message_bag):
		for function in file_functions:
			nb = len(function.lines.get_code_lines())

			if self.is_function_empty(function):
				message_string = self.config_reader.get("codesize", "empty_function", function.name)
				message_bag.add_warning(self, message_string, function.line_number)
			
			elif nb > Reviewer.ERROR_MAX_FUNCTION_LINE_NUMBER:
				message_string = self.config_reader.get("codesize", "too_many_lines_in_function_error", Reviewer.ERROR_MAX_FUNCTION_LINE_NUMBER, function.name, nb)
				message_bag.add_error(self, message_string, function.line_number)
			
			elif nb > Reviewer.WARN_MAX_FUNCTION_LINE_NUMBER:
				message_string = self.config_reader.get("codesize", "too_many_lines_in_function_warning", Reviewer.WARN_MAX_FUNCTION_LINE_NUMBER, function.name, nb)
				message_bag.add_warning(self, message_string, function.line_number)

	def review_variable_name_size(self, functions, message_bag):
		for function in functions:
			for var in function.variables:
				name = var.name
				line_number = var.line_number

				if variablelength.is_variable_name_too_short(name, function.body):
					message_string = self.config_reader.get("codesize", "variable_too_short_error", name)
					message_bag.add_error(self, message_string, line_number)
								
				if len(name) > Reviewer.WARN_MAX_NAME_SIZE:
					self.ouput_name_too_long_message("variable", name, line_number, message_bag)

	def ouput_name_too_long_message(self, type, name, line_number, message_bag):
		if len(name) > Reviewer.ERROR_MAX_NAME_SIZE:
			message_string = self.config_reader.get("codesize", "name_too_long_error", type, name, Reviewer.ERROR_MAX_NAME_SIZE, len(name))
			message_bag.add_error(self, message_string, line_number)
		
		elif len(name) > Reviewer.WARN_MAX_NAME_SIZE:
			message_string = self.config_reader.get("codesize", "name_too_long_warning", type, name, Reviewer.WARN_MAX_NAME_SIZE, len(name))
			message_bag.add_warning(self, message_string, line_number)

	def review_name_size(self, name, type, line_number, message_bag):
		if len(name) > Reviewer.WARN_MAX_NAME_SIZE:
			self.ouput_name_too_long_message(type, name, line_number, message_bag)
		
		if len(name) < Reviewer.ERROR_MIN_NAME_SIZE:
			message_string = self.config_reader.get("codesize", "name_too_short_error", type, name, Reviewer.ERROR_MIN_NAME_SIZE, len(name))
			message_bag.add_error(self, message_string, line_number)
		
		elif len(name) < Reviewer.WARN_MIN_NAME_SIZE:
			message_string = self.config_reader.get("codesize", "name_too_short_warning", type, name, Reviewer.WARN_MIN_NAME_SIZE, len(name))
			message_bag.add_warning(self, message_string, line_number)		

	def review_function_name_size(self, functions, message_bag):
		for function in functions:
			self.review_name_size(function.name, "function", function.line_number, message_bag)
			
	def review_arguments_name_size(self, functions, message_bag):
		for function in functions:
			for arg in function.signature:
				self.review_name_size(arg, "argument", function.line_number, message_bag)

	def review_class_properties_name_size(self, class_properties, message_bag):
		for property in class_properties:
			self.review_name_size(property.name, "class property", property.line_number, message_bag)

	def review(self, file_data, message_bag):
		self.review_line_number_in_file(file_data.lines, message_bag)
		self.review_line_number_in_functions(file_data.functions, message_bag)
		self.review_function_name_size(file_data.functions, message_bag)
		self.review_variable_name_size(file_data.functions, message_bag)
		self.review_nb_of_arguments(file_data.functions, message_bag)
		self.review_line_length(file_data.lines.all_lines, message_bag)
		self.review_arguments_name_size(file_data.functions, message_bag)
		self.review_class_properties_name_size(file_data.class_properties, message_bag)


if __name__ == "__main__":

	reviewer = Reviewer()

	assert reviewer.is_line_too_long("") == False
	assert reviewer.is_line_too_long("qisjd qosidhgiuq gsdigf qsdiughq isudhg qsdgo\n") == False
	assert reviewer.is_line_too_long("//3456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890\n") == False
	assert reviewer.is_line_too_long("//3456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890f") == True

	print "ALL TESTS OK"