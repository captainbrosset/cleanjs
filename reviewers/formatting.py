import re

from reviewers.base import BaseReviewer

class Reviewer(BaseReviewer):
	def review_statement_spacing(self, file_content, message_bag):
		bad_format = len(re.findall("[a-zA-Z0-9_$]+: function", file_content))
		bad_format += len(re.findall("[a-zA-Z0-9_$]+:function", file_content))
		bad_format += len(re.findall(":function\(", file_content))
		bad_format += len(re.findall(": function\(", file_content))
		bad_format += len(re.findall(":function \(", file_content))
		bad_format += len(re.findall("if\(", file_content))
		bad_format += len(re.findall("\)\{", file_content))
		
		if bad_format != 0:
			message_bag.add_error(self, "It seems you haven't properly formatted your file. Make sure you have installed the proper spket JS formatter and have pressed ctrl+shift+F")
	
	def review_empty_lines(self, file_content, message_bag):
		multiple_empty_lines_matches = re.finditer("\n[\s]*\n[\s]*\n", file_content)
		for match in multiple_empty_lines_matches:
			line_nb = self.get_line_nb_for_match_in_str(file_content, match)
			message_bag.add_warning(self, "There are several empty lines in a row, this probably means you are trying to space complex things up in an attempt to make them simpler ... why not making the code simpler first?", line_nb)
	
	def review_separator_comments(self, file_content, message_bag):
		# ----- or ////// or ******* or ######
		for match in re.finditer("---|###|\*\*\*|///|====", file_content):
			line_nb = self.get_line_nb_for_match_in_str(file_content, match)
			message_bag.add_warning(self, "You are using some kind of separator characters (####, ----, ////, ****), probably in an attempt to separate some complex code ... why not making it simpler in the first place?", line_nb)
	
	def review(self, file_data, message_bag):
		self.review_statement_spacing(file_data.content, message_bag)
		self.review_empty_lines(file_data.content, message_bag)
		self.review_separator_comments(file_data.content, message_bag)
		
