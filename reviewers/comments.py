import re

from commentsutils import similartocode

class Reviewer():
	MAX_CODE_COMMENT_RATIO_IN_FUNCTION = 0.3
	MAX_NUMBER_OF_SUBSEQUENT_COMMENTS_LINE = 2
	
	SEPARATOR_CHARACTERS = ["-", "\|", "!", "#", "\.", "\*", "=", "/", "~", "+", "\\"]
	MAX_NUMBER_OF_SEPARATOR_CHARACTERS_IN_COMMENTS = 3

	def get_name(self):
		return "comments"
		
	def get_help(self):
		return """The number, position and formatting of comments often indicates that code is not clean. An over-commented function for instance hides a complex and hard-to-read implementation.
		This reviewer checks:
		- if there are multiple comment lines in a row (starting with //)
		- the ratio of comments and code lines in functions (maximum at """ + str(Reviewer.MAX_CODE_COMMENT_RATIO_IN_FUNCTION) + """)
		- if there are comments just after an expression or statement block
		- if there are visual separator comment lines like // ****** in the code or similar"""

	def review_multiple_comment_lines(self, lines, message_bag):
		comments_lines_passed = 0
		line_nb_of_first_comment = -1
		is_in_jsdoc_style_comment = False
		
		for line in lines:
			
			if line.comments == "/**":
				is_in_jsdoc_style_comment = True
			if is_in_jsdoc_style_comment and line.comments == "*/":
				is_in_jsdoc_style_comment = False
		
			if not is_in_jsdoc_style_comment:
				if line.is_only_comments():			
					if line_nb_of_first_comment == -1:
						line_nb_of_first_comment = line.line_number
					comments_lines_passed += 1
				else:
					if comments_lines_passed > Reviewer.MAX_NUMBER_OF_SUBSEQUENT_COMMENTS_LINE:
						message_bag.add_warning(self, "You have " + str(comments_lines_passed) + " subsequent lines of comments in a row. Are you trying to explain something complex?", line_nb_of_first_comment)
						
					comments_lines_passed = 0
					line_nb_of_first_comment = -1
	
	def review_comments_ratio_in_functions(self, functions, message_bag):
		for function in functions:
			# FIXME: this is good because it uses the line_data already parsed for the function
			# FIXME: but will be problematic in case of constructor functions that have jsdoc'd fields
			# FIXME: because a lot of /** */ comment blocks will be there and should not be taken into account
			
			nb_comments_lines = len(function.lines.get_comments_lines())
			nb_total_lines = len(function.lines.get_code_lines()) + nb_comments_lines
			
			if nb_total_lines > 0:
				ratio = round(float(nb_comments_lines) / float(nb_total_lines), 1)
				if ratio > Reviewer.MAX_CODE_COMMENT_RATIO_IN_FUNCTION:
					message_bag.add_error(self, "There are more than " + str(int(Reviewer.MAX_CODE_COMMENT_RATIO_IN_FUNCTION*100)) + "% of comments in function " + function.name + " (" + str(ratio*100) + "%). Make the code simpler.", function.line_nb);
	
	def review_comments_after_statements(self, lines, message_bag):
		for line in lines:
			if line.is_both_code_and_comments():
				message_bag.add_warning(self, "Line has both code and comments. This is usually a sign that you need to explain a complex piece of code.", line.line_number)
		
	def review_separator_comments(self, lines, message_bag):
		maxn = "{" + str(Reviewer.MAX_NUMBER_OF_SEPARATOR_CHARACTERS_IN_COMMENTS) + "}"
		pattern = "-" + maxn + "|\|" + maxn + "|!" + maxn + "|#" + maxn + "|\." + maxn + "|\*" + maxn + "|=" + maxn + "|/" + maxn + "|~" + maxn + "|\+" + maxn
		
		for line in lines:
			if re.search(pattern, line.comments):
				message_bag.add_warning(self, "You are using some kind of separator characters in your comment, probably in an attempt to separate some complex code ... why not making it simpler in the first place?", line.line_number)
	
	def review_comment_code_similarity(self, lines, message_bag):
		for index, line in enumerate(lines):
			if line.is_only_comments() and lines[index+1].is_only_code():
				comment = line.complete_line
				code =  lines[index+1].complete_line
				if similartocode.is_code_and_comment_similar(code, comment):
					message_bag.add_warning(self, "It seems this comment is very similar to the code directly beneath it. Don't you think you can get rid of it?", line.line_number)

	def review(self, file_data, message_bag):
		self.review_multiple_comment_lines(file_data.lines.all_lines, message_bag)
		self.review_comments_ratio_in_functions(file_data.functions, message_bag)
		self.review_comments_after_statements(file_data.lines.all_lines, message_bag)
		self.review_separator_comments(file_data.lines.all_lines, message_bag)
		self.review_comment_code_similarity(file_data.lines.all_lines, message_bag)


if __name__ == "__main__":

	class MockBag:
		def __init__(self):
			self.warnings = []
		
		def add_warning(self, reviewer, message, line_number):
			self.warnings.append(line_number)
	
	class MockLine:
		def __init__(self, comments):
			self.comments = comments
			self.line_number = 0
		
	reviewer = Reviewer()
	bag = MockBag()	
	line1 = MockLine("this is something ..")
	line2 = MockLine("this is something ----")
	line3 = MockLine("this is something --#-~-")
	line4 = MockLine("// \\\\ ...")
	lines = []
	lines.append(line1)
	lines.append(line2)
	lines.append(line3)
	lines.append(line4)
	
	reviewer.review_separator_comments(lines, bag)
	
	assert len(bag.warnings) == 2, "Wrong number of separator comments found"
	
	print "ALL TESTS OK " + __file__