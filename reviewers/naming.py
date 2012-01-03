import re

from reviewers.base import BaseReviewer

class Reviewer(BaseReviewer):
	NB_OF_CHARS_IN_NAME_BEFORE_CAMELCASE = 10
	MAX_CONSONANT_VOWEL_RATIO = 5
	
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
	
	def _get_words_from_camelcase(self, str):
		return re.sub("([A-Z]+)", " \g<1>", str).lower().split(" ")
	
	def _get_consonant_vowel_ratio(self, str):
		consonant_nb = float(len(re.findall("q|w|r|t|p|s|d|f|g|h|j|k|l|z|x|c|v|b|n|m", str)))
		vowel_nb = float(len(re.findall("e|y|u|i|o|a", str)))
		if vowel_nb == 0:
			return float("inf")
		else:
			return consonant_nb / vowel_nb
	
	def review_function_name_meaning(self, functions, message_bag):
		for function in functions:
			name = function.name
			words = self._get_words_from_camelcase(name)
			for word in words:
				ratio = self._get_consonant_vowel_ratio(word)
				if ratio > Reviewer.MAX_CONSONANT_VOWEL_RATIO:
					message_bag.add_warning(self, "Word " + word + " inside function name " + name + " doesn't appear to mean anything.", function.line_nb)
			
	def review_camelcase_function_names(self, functions, message_bag):
		for function in functions:
			name = function.name
			parts = self._get_words_from_camelcase(name)
			if len(name) > Reviewer.NB_OF_CHARS_IN_NAME_BEFORE_CAMELCASE and len(parts) == 1:
				message_bag.add_warning(self, "Function name " + name + " doesn't appear to be camelcase", function.line_nb)
			
	def review(self, file_data, message_bag):
		self.review_gethasis_function_return(file_data.functions, message_bag)
		self.review_set_function_arg(file_data.functions, message_bag)
		self.review_camelcase_function_names(file_data.functions, message_bag)
		self.review_function_name_meaning(file_data.functions, message_bag)
		
		# FIXME: implement same camelcase and meaning checks for variables and <this...> fields