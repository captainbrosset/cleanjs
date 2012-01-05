import re

class Reviewer():
	MAX_CODE_COMMENT_RATIO_IN_FUNCTION = 0.3

	def get_name(self):
		return "comments"
		
	def get_help(self):
		return """The number, position and formatting of comments often indicates that code is not clean. An over-commented function for instance hides a complex and hard-to-read implementation.
		This reviewer checks:
		- if there are multiple comment lines in a row (starting with //)
		- the ratio of comments and code lines in functions (maximum at """ + str(Reviewer.MAX_CODE_COMMENT_RATIO_IN_FUNCTION) + """)
		- if there are comments just after an expression or statement block
		- if there are visual separator comment lines like // ****** in the code or similar"""

	def review_multiple_comment_lines(self, file_data, message_bag):
		matches = file_data.find_line_numbers("^[\s]*//.*\n^[\s]*//.*\n^[\s]*//.*", flags=re.MULTILINE)
		for match in matches:
			message_bag.add_warning(self, "It seems you have at least one block of // comments spanning over several lines. Are you trying to explain something complex?", match.line_number)
	
	def review_comments_ratio_in_functions(self, functions, message_bag):
		for function in functions:
			comment_lines = re.findall("^[\s]*//.*", function.body, flags=re.MULTILINE)
			total_lines = re.findall("^.*\S+.*$", function.body, flags=re.MULTILINE)
			if len(total_lines) == len(comment_lines):
				message_bag.add_warning(self, "There are only comments in function " + function.name + " (or maybe the function is empty). Is it really needed?", function.line_nb)
			else:
				ratio = float(len(comment_lines)) / float(len(total_lines))
				if ratio > Reviewer.MAX_CODE_COMMENT_RATIO_IN_FUNCTION:
					message_bag.add_error(self, "There are more than " + str(int(Reviewer.MAX_CODE_COMMENT_RATIO_IN_FUNCTION*100)) + "% of comments in function " + function.name + " (" + str(ratio*100) + "%). Make the code simpler.", function.line_nb);
	
	def review_comments_after_statements(self, lines, message_bag):
		for line_index, content in enumerate(lines):
			comments = re.findall(";[\s]*//|\}[\s]*//", content)
			if comments:
				message_bag.add_warning(self, "Line has comments after a statement or assignment. This is usually a sign that you need to explain a complex piece of code.", line_index+1)

	def review_separator_comments(self, file_data, message_bag):
		# ----- or ////// or ******* or ######
		matches = file_data.find_line_numbers("---|###|\*\*\*|///|====")
		for match in matches:
			message_bag.add_warning(self, "You are using some kind of separator characters (####, ----, ////, ****), probably in an attempt to separate some complex code ... why not making it simpler in the first place?", match.line_nb)
			
	def review(self, file_data, message_bag):
		self.review_multiple_comment_lines(file_data, message_bag)
		self.review_comments_ratio_in_functions(file_data.functions, message_bag)
		self.review_comments_after_statements(file_data.lines, message_bag)
		self.review_separator_comments(file_data, message_bag)