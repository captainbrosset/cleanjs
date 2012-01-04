import re

class Reviewer():
	def get_name(self):
		return "unused"
		
	def get_help(self):
		return """Variables or arguments which are not used clutter the code.
		This reviewer checks:
		- if all arguments of functions are used
		- if variables declared in functions are used"""

	def review_unused_arguments_in_functions(self, functions, message_bag):
		for function in functions:
			arguments = function.signature

			for argument in arguments:
				# FIXME: This is not enough because if anywhere the string <argument> is found, even if it's as a substring of a longer word, the reviewer won't output a message
				if function.body.find(argument) == -1:
					# FIXME: The line number passed is the one of the function, it would be better to find out the exact line number of the var assignment
					message_bag.add_error(self, "Argument " + argument + " in method " + function.name + " is never used", function.line_nb)
	
	def review_unused_variables_in_functions(self, functions, message_bag):
		for f in functions:
			variable_pattern = "var[\s]+([a-zA-Z0-9_$]+)"
			variables = re.findall(variable_pattern, f.body)
			body_without_variable_assignment = re.sub(variable_pattern, "", f.body)
			
			for variable in variables:
				# FIXME: This is not enough because if anywhere the string <variable> is found, even if it's as a substring of a longer word, the reviewer won't output a message
				if body_without_variable_assignment.find(variable) == -1:
					# FIXME: The line number passed is the one of the function, it would be better to find out the exact line number of the var assignment
					message_bag.add_error(self, "Variable " + variable + " in method " + f.name + " is declared but never used", f.line_nb)
		
	def review(self, file_data, message_bag):
		self.review_unused_variables_in_functions(file_data.functions, message_bag)
		self.review_unused_arguments_in_functions(file_data.functions, message_bag)