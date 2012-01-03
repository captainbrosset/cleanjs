import re

from reviewers.base import BaseReviewer

class Reviewer(BaseReviewer):
	NB_OF_CHARS_IN_NAME_BEFORE_CAMELCASE = 10
	
	def review_gethasis_function_return(self, functions, message_bag):
		for function in functions:
			name = function.name
			is_gethasis = (name[0:2] == "is" or name[0:3] == "has" or name[0:3] == "get")
			# FIXME: will fail on cases like this: var myVariableHasANameEndingWithReturn = 4;
			if is_gethasis and function.body.find("return ") == -1:
				message_bag.add_error(self, "Function " + name + " starts with 'is/has/get'. This usually means a return value is expected, but none was found.", function.line_nb);
	
	def review_set_function_arg(self, functions, message_bag):
		for function in functions:
			name = function.name
			is_set = (name[0:3] == "set")
			if is_set and len(function.signature) == 0:
				message_bag.add_error(self, "Function " + name + " starts with 'set'. This usually means an argument is passed, but none was found.", function.line_nb);
	
	def review_camelcase_function_names(self, functions, message_bag):
		for function in functions:
			name = function.name
			parts = re.sub("[A-Z]{1}", " ", name).split(" ")
			if len(name) > Reviewer.NB_OF_CHARS_IN_NAME_BEFORE_CAMELCASE and len(parts) == 1:
				message_bag.add_warning(self, "Function name " + name + " doesn't appear to be camelcase", function.line_nb)
			
	def review(self, file_data, message_bag):
		self.review_gethasis_function_return(file_data.functions, message_bag)
		self.review_set_function_arg(file_data.functions, message_bag)
		self.review_camelcase_function_names(file_data.functions, message_bag)
		# FIXME: implement this, should share the same code as the above method
		#self.review_camelcase_variable_names(file_data.variables, message_bag)