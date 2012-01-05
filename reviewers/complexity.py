import re

class Reviewer():
	WARN_MAX_NB_OF_STATEMENTS_IN_FUNCTION = 5
	ERROR_MAX_NB_OF_STATEMENTS_IN_FUNCTION = 10
	WARN_MAX_NB_OF_CONDITIONS_IN_IF = 1
	ERROR_MAX_NB_OF_CONDITIONS_IN_IF = 2
	
	def get_name(self):
		return "complexity"
		
	def get_help(self):
		return """Complex code is hard to read and maintain. Clean code should have small simple functions and classes that focus on one responsibility only, and their inner working should be simple to read.
		This reviewer checks:
		- the complexity of functions based on the number of if, for, while, switch statements (warning at """ + str(Reviewer.WARN_MAX_NB_OF_STATEMENTS_IN_FUNCTION) + """, error at """ + str(Reviewer.ERROR_MAX_NB_OF_STATEMENTS_IN_FUNCTION) + """)
		- the complexity of IF statements based on the number of conditions (warning at """ + str(Reviewer.WARN_MAX_NB_OF_CONDITIONS_IN_IF) + """, error at """ + str(Reviewer.ERROR_MAX_NB_OF_CONDITIONS_IN_IF) + """)"""
	
	def review_functions_complexity(self, functions, message_bag):
		for function in functions:
			statements = re.findall("if[\s]*\(|else[\s]*\(|else if[\s]*\(|while[\s]*\(|for[\s]*\(|switch[\s]*\(", function.body)
			if len(statements) > Reviewer.ERROR_MAX_NB_OF_STATEMENTS_IN_FUNCTION:
				message_bag.add_error(self, "Function " + function.name + " is too complex. There are too many statements involved in its logic", function.line_nb)
			elif len(statements) > Reviewer.WARN_MAX_NB_OF_STATEMENTS_IN_FUNCTION:
				message_bag.add_warning(self, "Function " + function.name + " is getting complex. There may be too much logic going on. Think about splitting.", function.line_nb)
	
	def review_ifs_complexity(self, file_data, message_bag):
		# TODO : change this to use the new file_data.find_line_number method, but this means that the method also needs to return the match groups too
		matches = file_data.find_line_numbers("if[\s]*\(([^\{]+)\{")
		for match in matches:
			line_nb = match.line_number
			conditions = re.findall("\|\||&&", match.match_object.group(1))
			if len(conditions) > Reviewer.ERROR_MAX_NB_OF_CONDITIONS_IN_IF:
				message_bag.add_error(self, "Found an IF statement with more than " + str(Reviewer.ERROR_MAX_NB_OF_CONDITIONS_IN_IF) + " AND or OR! Wrap them in a function like isABC()", line_nb)
			elif len(conditions) > Reviewer.WARN_MAX_NB_OF_CONDITIONS_IN_IF:
				message_bag.add_warning(self, "Found an IF statement with more than " + str(Reviewer.WARN_MAX_NB_OF_CONDITIONS_IN_IF) + " AND or OR! Could you extract this in a function like isABC()?", line_nb)
		
	def review(self, file_data, message_bag):
		self.review_functions_complexity(file_data.functions, message_bag)
		self.review_ifs_complexity(file_data, message_bag)