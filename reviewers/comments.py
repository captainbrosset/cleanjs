import re

from reviewers.base import BaseReviewer

class Reviewer(BaseReviewer):
	MAX_CODE_COMMENT_RATIO_IN_FUNCTION = 0.3

	def review_multiple_comment_lines(self, content, message_bag):
		multi_comments_matches = re.finditer("^[\s]*//.*\n^[\s]*//.*", content, flags=re.MULTILINE)
		for match in multi_comments_matches:
			line_nb = self.get_line_nb_for_match_in_str(content, match)
			message_bag.add_warning(self, "It seems you have at least one block of // comments spanning over several lines. Are you trying to explain something complex?", line_nb)
	
	def review_comments_ratio_in_functions(self, functions, message_bag):
		for function in functions:
			comment_lines = re.findall("^[\s]*//.*", function.body, flags=re.MULTILINE)
			total_lines = re.findall("^", function.body, flags=re.MULTILINE)
			ratio = float(len(comment_lines)) / float(len(total_lines))
			if ratio > Reviewer.MAX_CODE_COMMENT_RATIO_IN_FUNCTION:
				message_bag.add_error(self, "There are more than " + str(int(Reviewer.MAX_CODE_COMMENT_RATIO_IN_FUNCTION*100)) + "% of comments in function " + function.name + " (" + str(ratio*100) + "%). Make the code simpler.", function.line_nb);
	
	def review_comments_after_statements(self, lines, message_bag):
		for line_index, content in enumerate(lines):
			comments = re.findall(";[\s]*//|\}[\s]*//", content)
			if comments:
				message_bag.add_warning(self, "Line has comments after a statement or assignment. This is usually a sign that you need to explain a complex piece of code.", line_index+1)
	
	def review(self, file_data, message_bag):
		self.review_multiple_comment_lines(file_data.content, message_bag)
		self.review_comments_ratio_in_functions(file_data.functions, message_bag)
		self.review_comments_after_statements(file_data.lines, message_bag)