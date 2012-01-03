import re

from reviewers.base import BaseReviewer

class Reviewer(BaseReviewer):
	WARN_MAX_NB_OF_STATEMENTS_IN_FUNCTION = 5
	ERROR_MAX_NB_OF_STATEMENTS_IN_FUNCTION = 10
	WARN_MAX_NB_OF_CONDITIONS_IN_IF = 1
	ERROR_MAX_NB_OF_CONDITIONS_IN_IF = 2
	
	def review_functions_complexity(self, functions, message_bag):
		for function in functions:
			statements = re.findall("if[\s]*\(|else[\s]*\(|else if[\s]*\(|while[\s]*\(|for[\s]*\(|switch[\s]*\(", function.body)
			if len(statements) > Reviewer.ERROR_MAX_NB_OF_STATEMENTS_IN_FUNCTION:
				message_bag.add_error(self, "Function " + function.name + " is too complex. There are too many statements involved in its logic")
			elif len(statements) > Reviewer.WARN_MAX_NB_OF_STATEMENTS_IN_FUNCTION:
				message_bag.add_warning(self, "Function " + function.name + " is getting complex. There may be too much logic going on. Think about splitting.")
	
	def review_ifs_complexity(self, content, message_bag):
		ifs = re.findall("if[\s]*\(([^\{]+)\{", content)
		for an_if in ifs:
			conditions = re.findall("\|\||&&", an_if)
			if len(conditions) > Reviewer.ERROR_MAX_NB_OF_CONDITIONS_IN_IF:
				message_bag.add_error(self, "Found an IF statement with more than " + str(Reviewer.ERROR_MAX_NB_OF_CONDITIONS_IN_IF) + " AND or OR! Wrap them in a function like isABC()")
			elif len(conditions) > Reviewer.WARN_MAX_NB_OF_CONDITIONS_IN_IF:
				message_bag.add_warning(self, "Found an IF statement with more than " + str(Reviewer.WARN_MAX_NB_OF_CONDITIONS_IN_IF) + " AND or OR! Could you extract this in a funciton like isABC()?")
		
	def review(self, file_data, message_bag):
		self.review_functions_complexity(file_data.functions, message_bag)
		self.review_ifs_complexity(file_data.content, message_bag)