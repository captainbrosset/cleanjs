import urllib2
import logging
import re

logger = logging.getLogger(__name__)

LOCAL_DICTIONARY_FILE_NAME = "reviewers/namingutils/localdict.txt"
WORD_REFERENCE_API_KEY = "117b0"
WORD_REFERENCE_API_VERSION = "0.8"
WORD_REFERENCE_REQUEST_URL = "http://api.wordreference.com/" + WORD_REFERENCE_API_VERSION + "/" + WORD_REFERENCE_API_KEY + "/json/enfr/"

MAX_CONSONANT_VOWEL_RATIO = 5

def check_word_meaning_with_letter_ratio(word, dictionary_file=None):
	has_local_meaning = check_word_meaning_in_local_dict(word, dictionary_file)
	has_ratio_meaning = False
	if not has_local_meaning:
		consonant_nb = float(len(re.findall("q|w|r|t|p|s|d|f|g|h|j|k|l|z|x|c|v|b|n|m", word)))
		vowel_nb = float(len(re.findall("e|y|u|i|o|a", word)))
		ratio = float("inf")
		if vowel_nb != 0:
			ratio = consonant_nb / vowel_nb
		has_ratio_meaning = ratio < MAX_CONSONANT_VOWEL_RATIO
	return has_local_meaning or has_ratio_meaning

def check_word_meaning_with_dict(word, dictionary_file=None):
	has_local_meaning = check_word_meaning_in_local_dict(word, dictionary_file)
	has_remote_meaning = False
	if not has_local_meaning:
		logger.debug("word " + word + " was not found in local dict, looking online ... ")
		has_remote_meaning = check_word_meaning_in_remote_dict(word)
		if has_remote_meaning:
			logger.debug("word " + word + " was found online, adding to local dict ... ")
			add_word_to_local_dict(word, dictionary_file)
	return has_local_meaning or has_remote_meaning
	
def add_word_to_local_dict(word, dictionary_file=None):
	if dictionary_file:
		dictionary_file.write(word + "\n")
	else:
		dictionary_file = open(LOCAL_DICTIONARY_FILE_NAME, "a")
		dictionary_file.write(word + "\n")
		dictionary_file.close()

def check_word_meaning_in_local_dict(word, dictionary_file=None):
	should_file_be_closed = False
	
	if not dictionary_file:
		dictionary_file = open(LOCAL_DICTIONARY_FILE_NAME, "r")
		should_file_be_closed = True
	
	has_found_word = False
	dictionary_file.seek(0)
	for line in dictionary_file:
		line = line.replace("\n", "")
		if line == word:
			has_found_word = True
			break
	
	if should_file_be_closed:
		dictionary_file.close()
	
	return has_found_word

def check_word_meaning_in_remote_dict(word):
	response = urllib2.urlopen(WORD_REFERENCE_REQUEST_URL + word)
	response_text = response.read()
		
	# Note that we're not using any json lib here to avoid having dependencies (for GAE compat)
	is_not_word = response_text.find("NoTranslation") != -1
	
	if is_not_word:
		return False
	else:
		found_word = re.findall("\"OriginalTerm\" : \{ \"term\" : \"([a-zA-Z ]+)\"", response_text)[0]
		if found_word == word:
			return True
		else:
			return False


if __name__ == "__main__":
	import os
	
	assert check_word_meaning_in_remote_dict("test") == True, 1
	assert check_word_meaning_in_remote_dict("mgr") == False, 2
	assert check_word_meaning_in_remote_dict("ouhgzoihg") == False, 3
	assert check_word_meaning_in_remote_dict("chicken") == True, 4
	
	# FIXME: apparently first need to create the file with "w" mode, and then open it for read/write
	mock_dict_file = open("unit_test_mock_file.txt", "w")
	mock_dict_file.close()
	mock_dict_file = open("unit_test_mock_file.txt", "r+")
	
	assert check_word_meaning_in_local_dict("test", dictionary_file=mock_dict_file) == False, 5
	assert check_word_meaning_in_local_dict("manager", dictionary_file=mock_dict_file) == False, 6
	
	add_word_to_local_dict("test", mock_dict_file)
	
	assert check_word_meaning_in_local_dict("test", dictionary_file=mock_dict_file) == True, 7
	
	assert check_word_meaning_with_dict("something", dictionary_file=mock_dict_file) == True, 8
	assert check_word_meaning_with_dict("function", dictionary_file=mock_dict_file) == True, 9
	assert check_word_meaning_with_dict("nooooooo", dictionary_file=mock_dict_file) == False, 10
	assert check_word_meaning_with_dict("table", dictionary_file=mock_dict_file) == True, 11
		
	assert check_word_meaning_with_letter_ratio("cfghtr", dictionary_file=mock_dict_file) == False, 12
	assert check_word_meaning_with_letter_ratio("abeciw", dictionary_file=mock_dict_file) == True, 13
	assert check_word_meaning_with_letter_ratio("better", dictionary_file=mock_dict_file) == True, 14
	assert check_word_meaning_with_letter_ratio("mgr", dictionary_file=mock_dict_file) == False, 15
	
	mock_dict_file.close()
	os.remove("unit_test_mock_file.txt")
	
	print "ALL TESTS OK"