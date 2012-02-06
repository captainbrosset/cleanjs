import re

class Reviewer(object):
	def get_name(self):
		return "unused"
	
	def escape_identifier_for_regexp(self, name):
		return name.replace("$", "\$")
	
	def review_unused_arguments_in_functions(self, functions, message_bag):
		for function in functions:
			for argument in function.signature:
				if len(function.get_identifier_usage(argument)) == 0 and len(function.get_identifier_usage("arguments")) == 0:
					message_bag.add_error(self, "Argument " + argument + " in method " + function.name + " is never used", function.line_number)
				elif len(function.get_identifier_usage(argument)) == 0 and len(function.get_identifier_usage("arguments")) > 0:
					message_bag.add_warning(self, "Argument " + argument + " in method " + function.name + " is never directly used, only through the \"arguments\" keyword, this may make it harder to read", function.line_number)
	
	def review_unused_variables_in_functions(self, functions, message_bag):
		for function in functions:
			for var in function.variables:
				if len(function.get_identifier_usage(var.name)) == 1:
					message_bag.add_error(self, "Variable " + var.name + " in method " + function.name + " is declared but never used", var.line_number)
	
	def review_ununsed_class_properties(self, class_properties, lines, message_bag):
		for property in class_properties:
			occurences = []
			name = self.escape_identifier_for_regexp(property.name)
			for line in lines:
				occurences += re.findall("this\." + name + "[\s]*[=\(\]\)\.;$\+]{1}", line.code)
			if len(occurences) == 1:
				message_bag.add_error(self, "Class property " + property.name + " is initialized but never used", property.line_number)

	def review(self, file_data, message_bag):
		self.review_unused_variables_in_functions(file_data.functions, message_bag)
		self.review_unused_arguments_in_functions(file_data.functions, message_bag)
		self.review_ununsed_class_properties(file_data.class_properties, file_data.lines.all_lines, message_bag)


if __name__ == "__main__":
	print "NO TESTS TO RUN"