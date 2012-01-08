import re
import logging

from namingutils import wordmeaning

logger = logging.getLogger(__name__)

class Reviewer():
	NB_OF_CHARS_IN_NAME_BEFORE_CAMELCASE = 15
	MAX_CONSONANT_VOWEL_RATIO = 5
	REMOTE_WORD_CHECKING = True
	
	def get_name(self):
		return "naming"
		
	def get_help(self):
		return """Properly naming variables, arguments, functions or classes is key to making a code easy to read and maintain.
		This reviewer checks:
		- if a function returns something if its name starts with get, has or is
		- if a function accepts 1 argument if its name starts with set
		- if names are camelcased
		- if words in a camelcase name actually seem to mean something"""
	
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
		
	def _get_consonant_vowel_ratio(self, str):
		consonant_nb = float(len(re.findall("q|w|r|t|p|s|d|f|g|h|j|k|l|z|x|c|v|b|n|m", str)))
		vowel_nb = float(len(re.findall("e|y|u|i|o|a", str)))
		if vowel_nb == 0:
			return float("inf")
		else:
			return consonant_nb / vowel_nb
		
	def get_all_words_from_line(self, line):
		words = re.findall("[a-zA-Z]+", line)

		all_words = []
		for word in words:
			all_words += self.get_words_in_camelcase_str(word)
		return all_words
		
	def get_words_in_camelcase_str(self, str):
		if str == "":
			return []
		
		separated = re.sub("([A-Z]+)", " \g<1>", str).lower()
		if separated[0:1] == " ":
			separated = separated[1:]
		words = separated.split(" ")

		return words
	
	def review_all_names(self, all_lines, message_bag):
		for index, line in enumerate(all_lines):
			words_already_found = []
			words = self.get_all_words_from_line(line)
			
			for word in words:
				if word not in words_already_found and not wordmeaning.check_word_meaning(word):
					words_already_found.append(word)
					message_bag.add_error(self, "Word " + word + " doesn't mean anything", index+1)
	
	def review(self, file_data, message_bag):
		self.review_gethasis_function_return(file_data.functions, message_bag)
		self.review_set_function_arg(file_data.functions, message_bag)
		
		if Reviewer.REMOTE_WORD_CHECKING:
			self.review_all_names(file_data.lines.total_lines, message_bag)


if __name__ == "__main__":
	reviewer = Reviewer()
	
	assert reviewer.get_words_in_camelcase_str("") == [], 1
	assert reviewer.get_words_in_camelcase_str("simpletest") == ["simpletest"], 2
	assert reviewer.get_words_in_camelcase_str("simpleTest") == ["simple", "test"], 3
	assert reviewer.get_words_in_camelcase_str("SimpleTest") == ["simple", "test"], 4
	
	assert reviewer.get_all_words_from_line("// Project:   SproutCore - JavaScript Application Framework") == ["project","sprout","core","java","script","application","framework"], 5
	
	print "ALL TESTS OK"