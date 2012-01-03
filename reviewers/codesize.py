import re

from reviewers.base import BaseReviewer

class Reviewer(BaseReviewer):
	WARN_MAX_CLASS_LINE_NB = 150
	ERROR_MAX_CLASS_LINE_NB = 300
	WARN_MAX_METHOD_LINE_NB = 20
	ERROR_MAX_METHOD_LINE_NB = 50
	WARN_MIN_NAME_SIZE = 4
	ERROR_MIN_NAME_SIZE = 3
	WARN_MAX_NAME_SIZE = 30
	ERROR_MAX_NAME_SIZE = 50
	WARN_MAX_ARGUMENT_NB = 5
	ERROR_MAX_ARGUMENT_NB = 10
	ERROR_MAX_LINE_LENGTH = 120

	def review_line_length(self, file_content, message_bag):
		lines = re.split("\n", file_content)
		for index, line in enumerate(lines):
			if len(line) > Reviewer.ERROR_MAX_LINE_LENGTH:
				message_bag.add_error(self, "Line " + str(index+1) + " is more than " + str(Reviewer.ERROR_MAX_LINE_LENGTH) + " character long (" + str(len(line)) + "). This is hard to read.")

	def review_nb_of_arguments(self, functions, message_bag):
		for function in functions:
			if len(function.signature) > Reviewer.ERROR_MAX_ARGUMENT_NB:
				message_bag.add_error(self, "There are more than " + str(Reviewer.ERROR_MAX_ARGUMENT_NB) + " arguments in function " + function.name + " (" + str(len(function.signature)) + ")! Pass an object instead")
			elif len(function.signature) > Reviewer.WARN_MAX_ARGUMENT_NB:
				message_bag.add_warning(self, "There are more than " + str(Reviewer.WARN_MAX_ARGUMENT_NB) + " arguments in function " + function.name + " (" + str(len(function.signature)) + ")! Why not wrapping them in a nice class?")

	def review_line_nb_in_file(self, file_content, message_bag):
		lines = len(file_content.split("\n"))
		if lines > Reviewer.ERROR_MAX_CLASS_LINE_NB:
			message_bag.add_error(self, "There are more than " + str(Reviewer.ERROR_MAX_CLASS_LINE_NB) + " lines in the file (" + str(lines) + ") ! Surely the class is doing more than 1 thing")
		elif lines > Reviewer.WARN_MAX_CLASS_LINE_NB:
			message_bag.add_warning(self, "There are more than " + str(Reviewer.WARN_MAX_CLASS_LINE_NB) + " lines in the file (" + str(lines) + ") ! If possible, please try to refactor")

	def review_line_nb_in_methods(self, file_functions, message_bag):
		for method in file_functions:
			method_content = method.body
			method_name = method.name
			lines = len(method_content.split("\n"))
			if lines > Reviewer.ERROR_MAX_METHOD_LINE_NB:
				message_bag.add_error(self, "There are more than " + str(Reviewer.ERROR_MAX_METHOD_LINE_NB) + " lines in method " + method_name + " (" + str(lines) + ")! Surely the method is doing more than 1 thing")
			elif lines > Reviewer.WARN_MAX_METHOD_LINE_NB:
				message_bag.add_warning(self, "There are more than " + str(Reviewer.WARN_MAX_METHOD_LINE_NB) + " lines in method " + method_name + " (" + str(lines) + ")! If possible, please try to refactor it")

	def review_variable_name_size(self, variables, functions, message_bag):
		all_names = variables
		for f in functions:
			all_names.append(f.name)
		
		already_listed = []
		for name in all_names:
			if name not in already_listed:
				already_listed.append(name)
				if len(name) > Reviewer.ERROR_MAX_NAME_SIZE:
					message_bag.add_error(self, "The name of variable or method " + name + " is more than " + str(Reviewer.ERROR_MAX_NAME_SIZE) + " characters (" + str(len(name)) + "). This is too long")
				elif len(name) > Reviewer.WARN_MAX_NAME_SIZE:
					message_bag.add_warning(self, "The name of variable or method " + name + " is more than " + str(Reviewer.WARN_MAX_NAME_SIZE) + " characters (" + str(len(name)) + "). This may make it harder to read")
				if len(name) < Reviewer.ERROR_MIN_NAME_SIZE:
					message_bag.add_error(self, "The name of variable or method " + name + " is less than " + str(Reviewer.ERROR_MIN_NAME_SIZE) + " characters (" + str(len(name)) + "). This is way too short! Noone will understand what you mean")
				elif len(name) < Reviewer.WARN_MIN_NAME_SIZE:
					message_bag.add_warning(self, "The name of variable or method " + name + " is less than " + str(Reviewer.WARN_MIN_NAME_SIZE) + " characters (" + str(len(name)) + "). Think about making names self explanatory")

	def review(self, file_data, message_bag):
		self.review_line_nb_in_file(file_data.content, message_bag)
		self.review_line_nb_in_methods(file_data.functions, message_bag)
		self.review_variable_name_size(file_data.variables, file_data.functions, message_bag)
		self.review_nb_of_arguments(file_data.functions, message_bag)
		self.review_line_length(file_data.content, message_bag)