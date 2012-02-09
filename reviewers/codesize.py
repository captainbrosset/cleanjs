import re

from helpers import variablelength
from helpers import wordmeaning

class Reviewer():
	WARN_MAX_FILE_line_number = 150
	ERROR_MAX_FILE_line_number = 300
	WARN_MAX_FUNCTION_line_number = 20
	ERROR_MAX_FUNCTION_line_number = 50
	WARN_MIN_NAME_SIZE = 3
	ERROR_MIN_NAME_SIZE = 2
	WARN_MAX_NAME_SIZE = 35
	ERROR_MAX_NAME_SIZE = 50
	WARN_MAX_ARGUMENT_NB = 5
	ERROR_MAX_ARGUMENT_NB = 10
	ERROR_MAX_LINE_LENGTH = 120

	def get_name(self):
		return "code size"

	def is_line_too_long(self, line):
		if line[-1:] == "\n":
			line = line[0:-1]
		return len(line) > Reviewer.ERROR_MAX_LINE_LENGTH

	def review_line_length(self, lines, message_bag):
		for line in lines:
			if self.is_line_too_long(line.complete_line):
				message_bag.add_error(self, "Line is more than " + str(Reviewer.ERROR_MAX_LINE_LENGTH) + " character long (" + str(len(line.complete_line)) + "). This is hard to read.", line.line_number)

	def review_nb_of_arguments(self, functions, message_bag):
		for function in functions:
			if len(function.signature) > Reviewer.ERROR_MAX_ARGUMENT_NB:
				message_bag.add_error(self, "There are more than " + str(Reviewer.ERROR_MAX_ARGUMENT_NB) + " arguments in function " + function.name + " (" + str(len(function.signature)) + ")! Pass an object instead", function.line_number)
			elif len(function.signature) > Reviewer.WARN_MAX_ARGUMENT_NB:
				message_bag.add_warning(self, "There are more than " + str(Reviewer.WARN_MAX_ARGUMENT_NB) + " arguments in function " + function.name + " (" + str(len(function.signature)) + ")! Why not wrapping them in a nice class?", function.line_number)
	
	def review_line_number_in_file(self, lines, message_bag):
		# FIXME: comment lines are NOT ignored, should be?!
		nb = len(lines.all_lines)
		if nb > Reviewer.ERROR_MAX_FILE_line_number:
			message_bag.add_error(self, "There are more than " + str(Reviewer.ERROR_MAX_FILE_line_number) + " lines in the file (" + str(nb) + ") ! Surely the file has more than one responsibility", 1)
		elif nb > Reviewer.WARN_MAX_FILE_line_number:
			message_bag.add_warning(self, "There are more than " + str(Reviewer.WARN_MAX_FILE_line_number) + " lines in the file (" + str(nb) + ") ! If possible, please try to refactor", 1)

	def review_line_number_in_functions(self, file_functions, message_bag):
		for function in file_functions:			
			nb = len(function.lines.get_code_lines())
			if nb == 0:
				message_bag.add_warning(self, "Function " + function.name + " is empty. Is it really needed?", function.line_number)
			elif nb > Reviewer.ERROR_MAX_FUNCTION_line_number:
				message_bag.add_error(self, "There are more than " + str(Reviewer.ERROR_MAX_FUNCTION_line_number) + " lines in function " + function.name + " (" + str(nb) + ")! Surely the function has more than one responsibility", function.line_number)
			elif nb > Reviewer.WARN_MAX_FUNCTION_line_number:
				message_bag.add_warning(self, "There are more than " + str(Reviewer.WARN_MAX_FUNCTION_line_number) + " lines in function " + function.name + " (" + str(nb) + ")! If possible, please try to refactor it", function.line_number)

	def review_variable_name_size(self, functions, message_bag):
		for function in functions:
			for var in function.variables:
				name = var.name
				line_number = var.line_number

				if variablelength.is_variable_name_too_short(name, function.body):
					message_bag.add_error(self, "The name of variable " + name + " is too short", line_number)
				if len(name) > Reviewer.ERROR_MAX_NAME_SIZE:
					message_bag.add_error(self, "The name of variable " + name + " is more than " + str(Reviewer.ERROR_MAX_NAME_SIZE) + " characters (" + str(len(name)) + "). This is too long", line_number)
				elif len(name) > Reviewer.WARN_MAX_NAME_SIZE:
					message_bag.add_warning(self, "The name of variable " + name + " is more than " + str(Reviewer.WARN_MAX_NAME_SIZE) + " characters (" + str(len(name)) + "). This may make it harder to read", line_number)

	def review_name_size(self, name, type, line_number, message_bag):
		name_length = len(name)
		if name_length > Reviewer.ERROR_MAX_NAME_SIZE:
			message_bag.add_error(self, "The name of " + type + " " + name + " is more than " + str(Reviewer.ERROR_MAX_NAME_SIZE) + " characters (" + str(name_length) + "). This is too long", line_number)
		elif name_length > Reviewer.WARN_MAX_NAME_SIZE:
			message_bag.add_warning(self, "The name of " + type + " " + name + " is more than " + str(Reviewer.WARN_MAX_NAME_SIZE) + " characters (" + str(name_length) + "). This may make it harder to read", line_number)
		if name_length < Reviewer.ERROR_MIN_NAME_SIZE:
			message_bag.add_error(self, "The name of " + type + " " + name + " is less than " + str(Reviewer.ERROR_MIN_NAME_SIZE) + " characters (" + str(name_length) + "). This is way too short! Noone will understand what you mean", line_number)
		elif name_length < Reviewer.WARN_MIN_NAME_SIZE:
			message_bag.add_warning(self, "The name of " + type + " " + name + " is less than " + str(Reviewer.WARN_MIN_NAME_SIZE) + " characters (" + str(name_length) + "). Think about making names self explanatory", line_number)		

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

	print "ALL TESTS OK"