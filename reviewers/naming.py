import re

from reviewers.base import BaseReviewer

class Reviewer(BaseReviewer):
	def review_gethasis_function_return(self, functions, message_bag):
		for function in functions:
			name = function.name
			is_gethasis = (name[0:2] == "is" or name[0:3] == "has" or name[0:3] == "get")
			# FIXME: will fail on cases like this: var myVariableHasANameEndingWithReturn = 4;
			if is_gethasis and function.body.find("return ") == -1:
				message_bag.add_error(self, "Function " + name + " starts with 'is/has/get'. This usually means a return value is expected, but none was found.");
	
	def review_set_function_arg(self, functions, message_bag):
		for function in functions:
			name = function.name
			is_set = (name[0:3] == "set")
			if is_set and len(function.signature) == 0:
				message_bag.add_error(self, "Function " + name + " starts with 'set'. This usually means an argument is passed, but none was found.");
	
	def review(self, file_data, message_bag):
		self.review_gethasis_function_return(file_data.functions, message_bag)
		self.review_set_function_arg(file_data.functions, message_bag)