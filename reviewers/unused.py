import re

from reviewers.base import BaseReviewer

class Reviewer(BaseReviewer):
	def review_unused_variables_in_functions(self, functions, message_bag):
		for f in functions:
			variable_pattern = "var[\s]+([a-zA-Z0-9_$]+)"
			variables = re.findall(variable_pattern, f.body)
			body_without_variable_assignment = re.sub(variable_pattern, "", f.body)
			
			for variable in variables:
				if body_without_variable_assignment.find(variable) == -1:
					# FIXME: The line number passed is the one of the function, it would be better to find out the exact line number of the var assignment
					message_bag.add_error(self, "Variable " + variable + " in method " + f.name + " is declared but never used", f.line_nb)
		
	def review(self, file_data, message_bag):
		self.review_unused_variables_in_functions(file_data.functions, message_bag)