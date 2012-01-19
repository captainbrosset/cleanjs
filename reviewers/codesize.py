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

	def review_variable_name_size(self, functions, message_bag):
		# FIXME: should take into account the "scope" of the variable
		# Indeed, if the variable is only used in a few lines of codes, close together, then it's fine to be short
		# There should be some kind of relation between the variable name and the number of lines it is used in


		

		# Listing functions only
		# TODO: work in progress. Trying to act at function level, to avoid having to care about scopes
		# For each function, check variables, for each var, check the body to find out where it appears
		for function in functions:
			for var in function.variables:
				pass

		"""
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
		"""

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
		self.review_variable_name_size(file_data.functions, message_bag)
		self.review_nb_of_arguments(file_data.functions, message_bag)
		self.review_line_length(file_data.lines.all_lines, message_bag)


if __name__ == "__main__":
	
	reviewer = Reviewer()

	class MockFunction(object):
		def __init__(self, name, signature, body, lines, variables, line_nb):
			self.name = name
			self.signature = signature
			self.body = body
			self.lines = lines
			self.variables = variables
			self.line_nb = line_nb
	
	class MockBag(object):
		def __init__(self):
			pass

	class MockVariable(object):
		def __init__(self, name, line_nb):
			self.name = name
			self.line_nb = line_nb

	var_test = MockVariable("test", 32)
	var_i = MockVariable("i", 33)
	var_j = MockVariable("j", 39)
	function_body = """
	var test = 5;
	for(var i=0; i < test; i++) {
		alert("test" + i);
	}

	test ++;

	var j = true;
	while(j) {
		if(5%1) {
			test ++;
		} else {
			break;
		}
	}

	if(j) {
		// do something
	}
	"""
	function1 = MockFunction("myfun", [], function_body, {}, [var_test, var_i, var_j], 30)

	bag = MockBag()
	reviewer.review_variable_name_size([function1], bag)

	# TODO: work in progress here -> create asserts that should make sure that errors/warnings are thrown for variables too long
	# But also, make sure that errors are thrown for variables too short, depending on their scope span
	# --> 1/2 letter(s) variables only accepted if not spanning over more than 3 consecutive lines ??

	print "ALL TESTS OK " + __file__