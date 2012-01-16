import re

class Reviewer():
	WARN_MAX_FILE_LINE_NB = 150
	ERROR_MAX_FILE_LINE_NB = 300
	WARN_MAX_FUNCTION_LINE_NB = 20
	ERROR_MAX_FUNCTION_LINE_NB = 50
	WARN_MIN_NAME_SIZE = 3
	ERROR_MIN_NAME_SIZE = 2
	WARN_MAX_NAME_SIZE = 30
	ERROR_MAX_NAME_SIZE = 50
	WARN_MAX_ARGUMENT_NB = 5
	ERROR_MAX_ARGUMENT_NB = 10
	ERROR_MAX_LINE_LENGTH = 120

	def get_name(self):
		return "code size"
		
	def get_help(self):
		return """The size of code is a good indicator of its quality. The fact that the size of various elements of the code is small indicates that it's easy to understand.
		This reviewer checks:
		- length of lines (max is """ + str(Reviewer.ERROR_MAX_LINE_LENGTH) + """)
		- number of arguments in function signatures (warning at """ + str(Reviewer.WARN_MAX_ARGUMENT_NB) + """, error at """ + str(Reviewer.ERROR_MAX_ARGUMENT_NB) + """)
		- number of total lines of code in the file (warning at """ + str(Reviewer.WARN_MAX_FILE_LINE_NB) + """, error at """ + str(Reviewer.ERROR_MAX_FILE_LINE_NB) + """)
		- number of total lines of code in functions (warning at """ + str(Reviewer.WARN_MAX_FUNCTION_LINE_NB) + """, error at """ + str(Reviewer.ERROR_MAX_FUNCTION_LINE_NB) + """)
		- length of variable names (warning when > """ + str(Reviewer.WARN_MAX_NAME_SIZE) + """ or < """ + str(Reviewer.WARN_MIN_NAME_SIZE) + """, error when > """ + str(Reviewer.ERROR_MAX_NAME_SIZE) + """ or < """ + str(Reviewer.ERROR_MIN_NAME_SIZE) + """)
		- length of function names (same as above)"""

	def review_line_length(self, lines, message_bag):
		for line in lines:
			if len(line.complete_line) > Reviewer.ERROR_MAX_LINE_LENGTH:
				message_bag.add_error(self, "Line is more than " + str(Reviewer.ERROR_MAX_LINE_LENGTH) + " character long (" + str(len(line.complete_line)) + "). This is hard to read.", line.line_number)

	def review_nb_of_arguments(self, functions, message_bag):
		for function in functions:
			if len(function.signature) > Reviewer.ERROR_MAX_ARGUMENT_NB:
				message_bag.add_error(self, "There are more than " + str(Reviewer.ERROR_MAX_ARGUMENT_NB) + " arguments in function " + function.name + " (" + str(len(function.signature)) + ")! Pass an object instead", function.line_nb)
			elif len(function.signature) > Reviewer.WARN_MAX_ARGUMENT_NB:
				message_bag.add_warning(self, "There are more than " + str(Reviewer.WARN_MAX_ARGUMENT_NB) + " arguments in function " + function.name + " (" + str(len(function.signature)) + ")! Why not wrapping them in a nice class?", function.line_nb)

	def review_line_nb_in_file(self, lines, message_bag):
		# FIXME: comment lines are NOT ignored, should be?!
		nb = len(lines.all_lines)
		if nb > Reviewer.ERROR_MAX_FILE_LINE_NB:
			message_bag.add_error(self, "There are more than " + str(Reviewer.ERROR_MAX_FILE_LINE_NB) + " lines in the file (" + str(nb) + ") ! Surely the file is doing more than 1 thing")
		elif nb > Reviewer.WARN_MAX_FILE_LINE_NB:
			message_bag.add_warning(self, "There are more than " + str(Reviewer.WARN_MAX_FILE_LINE_NB) + " lines in the file (" + str(nb) + ") ! If possible, please try to refactor")

	def review_line_nb_in_functions(self, file_functions, message_bag):
		for function in file_functions:
			# FIXME: comment lines are NOT ignored, should be?!
			# Should use the lines_data
			
			nb = len(function.lines.get_code_lines())
			if nb == 0:
				message_bag.add_warning(self, "Function " + function.name + " is empty. Is it really needed?", function.line_nb)
			elif nb > Reviewer.ERROR_MAX_FUNCTION_LINE_NB:
				message_bag.add_error(self, "There are more than " + str(Reviewer.ERROR_MAX_FUNCTION_LINE_NB) + " lines in function " + function.name + " (" + str(nb) + ")! Surely the function is doing more than 1 thing", function.line_nb)
			elif nb > Reviewer.WARN_MAX_FUNCTION_LINE_NB:
				message_bag.add_warning(self, "There are more than " + str(Reviewer.WARN_MAX_FUNCTION_LINE_NB) + " lines in function " + function.name + " (" + str(nb) + ")! If possible, please try to refactor it", function.line_nb)

	def review_variable_name_size(self, variables, message_bag):
		# FIXME: should be merged with review_function_name_size and should find line numbers
		already_listed = []
		for variable in variables:
			name = variable.name
			if name not in already_listed:
				already_listed.append(name)
				if len(name) > Reviewer.ERROR_MAX_NAME_SIZE:
					message_bag.add_error(self, "The name of variable " + name + " is more than " + str(Reviewer.ERROR_MAX_NAME_SIZE) + " characters (" + str(len(name)) + "). This is too long", variable.line_nb)
				elif len(name) > Reviewer.WARN_MAX_NAME_SIZE:
					message_bag.add_warning(self, "The name of variable " + name + " is more than " + str(Reviewer.WARN_MAX_NAME_SIZE) + " characters (" + str(len(name)) + "). This may make it harder to read", variable.line_nb)
				if len(name) < Reviewer.ERROR_MIN_NAME_SIZE:
					message_bag.add_error(self, "The name of variable " + name + " is less than " + str(Reviewer.ERROR_MIN_NAME_SIZE) + " characters (" + str(len(name)) + "). This is way too short! Noone will understand what you mean", variable.line_nb)
				elif len(name) < Reviewer.WARN_MIN_NAME_SIZE:
					message_bag.add_warning(self, "The name of variable " + name + " is less than " + str(Reviewer.WARN_MIN_NAME_SIZE) + " characters (" + str(len(name)) + "). Think about making names self explanatory", variable.line_nb)

	def review_function_name_size(self, functions, message_bag):
		for function in functions:
			name_length = len(function.name)
			if name_length > Reviewer.ERROR_MAX_NAME_SIZE:
				message_bag.add_error(self, "The name of function " + function.name + " is more than " + str(Reviewer.ERROR_MAX_NAME_SIZE) + " characters (" + str(name_length) + "). This is too long", function.line_nb)
			elif name_length > Reviewer.WARN_MAX_NAME_SIZE:
				message_bag.add_warning(self, "The name of function " + function.name + " is more than " + str(Reviewer.WARN_MAX_NAME_SIZE) + " characters (" + str(name_length) + "). This may make it harder to read", function.line_nb)
			if name_length < Reviewer.ERROR_MIN_NAME_SIZE:
				message_bag.add_error(self, "The name of function " + function.name + " is less than " + str(Reviewer.ERROR_MIN_NAME_SIZE) + " characters (" + str(name_length) + "). This is way too short! Noone will understand what you mean", function.line_nb)
			elif name_length < Reviewer.WARN_MIN_NAME_SIZE:
				message_bag.add_warning(self, "The name of function " + function.name + " is less than " + str(Reviewer.WARN_MIN_NAME_SIZE) + " characters (" + str(name_length) + "). Think about making names self explanatory", function.line_nb)

	def review(self, file_data, message_bag):
		self.review_line_nb_in_file(file_data.lines, message_bag)
		self.review_line_nb_in_functions(file_data.functions, message_bag)
		self.review_function_name_size(file_data.functions, message_bag)
		self.review_variable_name_size(file_data.variables, message_bag)
		self.review_nb_of_arguments(file_data.functions, message_bag)
		self.review_line_length(file_data.lines.all_lines, message_bag)


if __name__ == "__main__":
	print "NO TESTS TO RUN " + __file__