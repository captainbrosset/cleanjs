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
			for argument in function.signature:
				before_after_arg = "[ \t\[\]\(\)\.\+\-\{\};:,]{1}"
				occurences = re.findall(before_after_arg + argument + before_after_arg, function.body)
				if len(occurences) == 0:
					message_bag.add_error(self, "Argument " + argument + " in method " + function.name + " is never used", function.line_nb)
	
	def review_unused_variables_in_functions(self, functions, message_bag):
		for function in functions:
			for var in function.variables:
				before_after_var = "[ \t\[\]\(\)\.\+\-\{\};:,]{1}"
				occurences = re.findall(before_after_var + var.name + before_after_var, function.body)
				if len(occurences) == 1:
					message_bag.add_error(self, "Variable " + var.name + " in method " + function.name + " is declared but never used", var.line_nb)
		
	def review(self, file_data, message_bag):
		self.review_unused_variables_in_functions(file_data.functions, message_bag)
		self.review_unused_arguments_in_functions(file_data.functions, message_bag)


if __name__ == "__main__":
	print "NO TESTS TO RUN"