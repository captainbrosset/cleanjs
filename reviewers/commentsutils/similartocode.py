# Tricking the PYTHONPATH because relative imports don't work when running the file standalone
import sys
sys.path.append("../")
sys.path.append("./reviewers")

import re

from namingutils import extractwords

def get_unique_words(words):
	return list(set(words))

def is_code_and_comment_similar(code, comment):
	comment_words = get_unique_words(extractwords.get_all_words_from_line(comment))
	comment_words_similar_to_code = []
	code_words = get_unique_words(extractwords.get_all_words_from_line(code))
	code_words_similar_to_comment = []

	if len(comment_words) == 0 or len(code_words) == 0:
		return False

	for word in comment_words:
		if word in code_words:
			comment_words_similar_to_code.append(word)

	for word in code_words:
		if word in comment_words:
			code_words_similar_to_comment.append(word)
	
	comment_ratio = float(len(comment_words_similar_to_code)) / float(len(comment_words))
	code_ratio = float(len(code_words_similar_to_comment)) / float(len(code_words))

	return (comment_ratio >= 0.6 and code_ratio >= 0.6) or (comment_ratio >= 0.5 and code_ratio >= 0.8) or (code_ratio >= 0.5 and comment_ratio >= 0.8)

if __name__ == "__main__":

	comment = "// Print the array to the standard output"
	code = "this.printArrayToOutput(array);"
	assert is_code_and_comment_similar(code, comment) == True, "The comment is almost exactly like the code, should be detected as similar"

	comment = """/**
	* Class my.package.TestCase
	* This class handles test cases objects
	* Extend from this class to create your test cases
	*/
	"""
	code = "my.package.TestCase = function(suite) {"
	assert is_code_and_comment_similar(code, comment) == False, "Comment looks like jsdoc, should not be detected as similar to the code"

	comment = "// changed because of bug #34, need to check for words"
	code = "var isMatch = string.match(/[a-z]/gi);"
	assert is_code_and_comment_similar(code, comment) == False, "The line of comment gives extra explanation, should not be detected as similar to the code"

	comment = "// Resize a photo to the max dim but not if smaller"
	code = "self._resizeAPhoto(photo, maxDim, noResizeIfSmaller);"
	assert is_code_and_comment_similar(code, comment) == True, "The comment is almost exactly like the code, should be detected as similar"

	print "ALL TESTS OK " + __file__