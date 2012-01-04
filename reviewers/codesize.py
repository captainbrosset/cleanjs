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

	def review_line_length(self, file_content, message_bag):
		lines = re.split("\n", file_content)
		for index, line in enumerate(lines):
			if len(line) > Reviewer.ERROR_MAX_LINE_LENGTH:
				message_bag.add_error(self, "Line is more than " + str(Reviewer.ERROR_MAX_LINE_LENGTH) + " character long (" + str(len(line)) + "). This is hard to read.", index+1)

	def review_nb_of_arguments(self, functions, message_bag):
		for function in functions:
			if len(function.signature) > Reviewer.ERROR_MAX_ARGUMENT_NB:
				message_bag.add_error(self, "There are more than " + str(Reviewer.ERROR_MAX_ARGUMENT_NB) + " arguments in function " + function.name + " (" + str(len(function.signature)) + ")! Pass an object instead", function.line_nb)
			elif len(function.signature) > Reviewer.WARN_MAX_ARGUMENT_NB:
				message_bag.add_warning(self, "There are more than " + str(Reviewer.WARN_MAX_ARGUMENT_NB) + " arguments in function " + function.name + " (" + str(len(function.signature)) + ")! Why not wrapping them in a nice class?", function.line_nb)

	def review_line_nb_in_file(self, file_content, message_bag):
		# FIXME: comment lines are NOT ignored, should be?!
		lines = len(re.findall("^.*\S+.*$", file_content, flags=re.MULTILINE))
		if lines > Reviewer.ERROR_MAX_FILE_LINE_NB:
			message_bag.add_error(self, "There are more than " + str(Reviewer.ERROR_MAX_FILE_LINE_NB) + " lines in the file (" + str(lines) + ") ! Surely the class is doing more than 1 thing")
		elif lines > Reviewer.WARN_MAX_FILE_LINE_NB:
			message_bag.add_warning(self, "There are more than " + str(Reviewer.WARN_MAX_FILE_LINE_NB) + " lines in the file (" + str(lines) + ") ! If possible, please try to refactor")

	def review_line_nb_in_functions(self, file_functions, message_bag):
		for function in file_functions:
			# FIXME: comment lines are NOT ignored, should be?!
			lines = len(re.findall("^.*\S+.*$", function.body, flags=re.MULTILINE))
			if lines == 0:
				message_bag.add_warning(self, "Function " + function.name + " is empty. Is it really needed?", function.line_nb)
			elif lines > Reviewer.ERROR_MAX_FUNCTION_LINE_NB:
				message_bag.add_error(self, "There are more than " + str(Reviewer.ERROR_MAX_FUNCTION_LINE_NB) + " lines in function " + function.name + " (" + str(lines) + ")! Surely the function is doing more than 1 thing", function.line_nb)
			elif lines > Reviewer.WARN_MAX_FUNCTION_LINE_NB:
				message_bag.add_warning(self, "There are more than " + str(Reviewer.WARN_MAX_FUNCTION_LINE_NB) + " lines in function " + function.name + " (" + str(lines) + ")! If possible, please try to refactor it", function.line_nb)

	def review_variable_name_size(self, variables, message_bag):
		# FIXME: should be merged with review_function_name_size and should find line numbers
		already_listed = []
		for name in variables:
			if name not in already_listed:
				already_listed.append(name)
				if len(name) > Reviewer.ERROR_MAX_NAME_SIZE:
					message_bag.add_error(self, "The name of variable " + name + " is more than " + str(Reviewer.ERROR_MAX_NAME_SIZE) + " characters (" + str(len(name)) + "). This is too long")
				elif len(name) > Reviewer.WARN_MAX_NAME_SIZE:
					message_bag.add_warning(self, "The name of variable " + name + " is more than " + str(Reviewer.WARN_MAX_NAME_SIZE) + " characters (" + str(len(name)) + "). This may make it harder to read")
				if len(name) < Reviewer.ERROR_MIN_NAME_SIZE:
					message_bag.add_error(self, "The name of variable " + name + " is less than " + str(Reviewer.ERROR_MIN_NAME_SIZE) + " characters (" + str(len(name)) + "). This is way too short! Noone will understand what you mean")
				elif len(name) < Reviewer.WARN_MIN_NAME_SIZE:
					message_bag.add_warning(self, "The name of variable " + name + " is less than " + str(Reviewer.WARN_MIN_NAME_SIZE) + " characters (" + str(len(name)) + "). Think about making names self explanatory")

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
		self.review_line_nb_in_file(file_data.content, message_bag)
		self.review_line_nb_in_functions(file_data.functions, message_bag)
		self.review_function_name_size(file_data.functions, message_bag)
		self.review_variable_name_size(file_data.variables, message_bag)
		self.review_nb_of_arguments(file_data.functions, message_bag)
		self.review_line_length(file_data.content, message_bag)