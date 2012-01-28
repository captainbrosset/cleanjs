import re

class Reviewer():
	WARN_MAX_NB_OF_STATEMENTS_IN_FUNCTION = 5
	ERROR_MAX_NB_OF_STATEMENTS_IN_FUNCTION = 10
	WARN_MAX_NB_OF_CONDITIONS_IN_IF = 1
	ERROR_MAX_NB_OF_CONDITIONS_IN_IF = 2
	ERROR_MAX_NB_OF_RETURNS_IN_FUNCTION = 5
	WARN_MAX_NB_OF_RETURNS_IN_FUNCTION = 2
	
	def get_name(self):
		return "complexity"
	
	def review_functions_complexity(self, functions, message_bag):
		for function in functions:
			statements = re.findall("if[\s]*\(|else[\s]*\{|else if[\s]*\(|while[\s]*\(|for[\s]*\(|switch[\s]*\(", function.body)
			if len(statements) > Reviewer.ERROR_MAX_NB_OF_STATEMENTS_IN_FUNCTION:
				message_bag.add_error(self, "Function " + function.name + " is too complex. There are too many statements involved in its logic", function.line_nb)
			elif len(statements) > Reviewer.WARN_MAX_NB_OF_STATEMENTS_IN_FUNCTION:
				message_bag.add_warning(self, "Function " + function.name + " is getting complex. There may be too much logic going on. Think about splitting.", function.line_nb)
			
			returns = re.findall("return ", function.body)
			if len(returns) > Reviewer.ERROR_MAX_NB_OF_RETURNS_IN_FUNCTION:
				message_bag.add_error(self, "Function " + function.name + " returns more than " + str(Reviewer.ERROR_MAX_NB_OF_RETURNS_IN_FUNCTION) + " values (" + str(len(returns)) + ").", function.line_nb)
			elif len(returns) > Reviewer.WARN_MAX_NB_OF_RETURNS_IN_FUNCTION:
				message_bag.add_warning(self, "Function " + function.name + " returns more than " + str(Reviewer.WARN_MAX_NB_OF_RETURNS_IN_FUNCTION) + " values (" + str(len(returns)) + ").", function.line_nb)
	
	def review_ifs_complexity(self, lines, message_bag):
		for line in lines:
			if line.has_code():
				conditions = re.findall("\|\||&&", line.code)
				if len(conditions) > Reviewer.ERROR_MAX_NB_OF_CONDITIONS_IN_IF:
					message_bag.add_error(self, "Found an IF statement with more than " + str(Reviewer.ERROR_MAX_NB_OF_CONDITIONS_IN_IF) + " AND or OR! Wrap them in a function like isABC()", line.line_number)
				elif len(conditions) > Reviewer.WARN_MAX_NB_OF_CONDITIONS_IN_IF:
					message_bag.add_warning(self, "Found an IF statement with more than " + str(Reviewer.WARN_MAX_NB_OF_CONDITIONS_IN_IF) + " AND or OR! Could you extract this in a function like isABC()?", line.line_number)
	
	def review(self, file_data, message_bag):
		self.review_functions_complexity(file_data.functions, message_bag)
		self.review_ifs_complexity(file_data.lines.all_lines, message_bag)
		
		
if __name__ == "__main__":
	print "NO TESTS TO RUN"