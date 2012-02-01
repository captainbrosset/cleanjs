import re

class Reviewer():
	def get_name(self):
		return "unused"
	
	def review_unused_arguments_in_functions(self, functions, message_bag):
		for function in functions:
			for argument in function.signature:

				before_after_arg = "[\s\[\]\(\)\.\+\-\{\};:,]{1}"
				argument = argument.replace("$", "\$")
				occurences = re.findall(before_after_arg + argument + before_after_arg, function.lines.get_whole_code())

				if len(occurences) == 0:
					message_bag.add_error(self, "Argument " + argument + " in method " + function.name + " is never used", function.line_number)
	
	def review_unused_variables_in_functions(self, functions, message_bag):
		for function in functions:
			for var in function.variables:
				var_name = var.name.replace("$", "\$")
				before_after_var = "[\s\[\]\(\)\.\+\-\{\};:,]{1}"
				occurences = re.findall(before_after_var + var_name + before_after_var, function.lines.get_whole_code())
				if len(occurences) == 1:
					message_bag.add_error(self, "Variable " + var_name + " in method " + function.name + " is declared but never used", var.line_number)
		
	def review(self, file_data, message_bag):
		self.review_unused_variables_in_functions(file_data.functions, message_bag)
		self.review_unused_arguments_in_functions(file_data.functions, message_bag)


if __name__ == "__main__":
	print "NO TESTS TO RUN"