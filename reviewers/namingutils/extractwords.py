import re

def get_all_words_from_line(line):
	words = re.findall("[a-zA-Z]+", line)

	all_words = []
	for word in words:
		all_words += get_words_in_camelcase_str(word)
	return all_words
		
def get_words_in_camelcase_str(str):
	if str == "":
		return []
		
	separated = re.sub("([A-Z]+)([A-Z]{1}[a-z]+)", " \g<1> \g<2>", str)
	separated = re.sub("([A-Z]+)", " \g<1>", separated).lower()

	parts = separated.split(" ")
	words = []
	for part in parts:
		if part != "":
			words.append(part)

	return words

if __name__ == "__main__":
	assert get_all_words_from_line("this is a veryLongLine of jsCODE") == ["this", "is", "a", "very", "long", "line", "of", "js", "code"], "line words not extracted"
	assert get_all_words_from_line("self._resizeAPhoto(photo, maxDim, noResizeIfSmaller);") == ["self", "resize", "a", "photo", "photo", "max", "dim", "no", "resize", "if", "smaller"]

	assert get_words_in_camelcase_str("resizeAPhoto") == ["resize", "a", "photo"], 0
	assert get_words_in_camelcase_str("") == [], 1
	assert get_words_in_camelcase_str("simpletest") == ["simpletest"], 2
	assert get_words_in_camelcase_str("simpleTest") == ["simple", "test"], 3
	assert get_words_in_camelcase_str("SimpleTest") == ["simple", "test"], 4
	assert get_words_in_camelcase_str("asyncXHR") == ["async", "xhr"], 4
		
	print "ALL TESTS OK " + __file__