import json
import urllib2
import logging

logger = logging.getLogger(__name__)

LOCAL_DICTIONARY_FILE_NAME = "reviewers/namingutils/localdict.txt"
WORD_REFERENCE_API_KEY = "117b0"
WORD_REFERENCE_API_VERSION = "0.8"
WORD_REFERENCE_REQUEST_URL = "http://api.wordreference.com/" + WORD_REFERENCE_API_VERSION + "/" + WORD_REFERENCE_API_KEY + "/json/enfr/"

def check_word_meaning(word, dictionary_file=None):
	if not check_word_structure(word):
		return False
	has_local_meaning = check_word_meaning_locally(word, dictionary_file)
	has_remote_meaning = False
	if not has_local_meaning:
		logger.debug("word " + word + " was not found in local dict, looking online ... ")
		has_remote_meaning = check_word_meaning_remotely(word)
		if has_remote_meaning:
			logger.debug("word " + word + " was found online, adding to local dict ... ")
			add_local_word(word, dictionary_file)
	return has_local_meaning or has_remote_meaning
	
def add_local_word(word, dictionary_file=None):
	if dictionary_file:
		dictionary_file.write(word + "\n")
	else:
		dictionary_file = open(LOCAL_DICTIONARY_FILE_NAME, "a")
		dictionary_file.write(word + "\n")
		dictionary_file.close()

def check_word_structure(word):
	if len(word) == 1 and (word != "a" or word != "i"):
		return False
	return True

def check_word_meaning_locally(word, dictionary_file=None):
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

def check_word_meaning_remotely(word):
	response = urllib2.urlopen(WORD_REFERENCE_REQUEST_URL + word)
	response_text = response.read()
	response_object = json.loads(response_text)
	
	if response_object.has_key("Error"):
		return False
	else:
		if response_object.has_key("PrincipalTranslations"):
			if response_object["PrincipalTranslations"][0].has_key("OriginalTerm"):
				if response_object["PrincipalTranslations"][0]["OriginalTerm"]["term"] != word:
					return False
				else:
					return True


if __name__ == "__main__":
	import os
	
	assert check_word_meaning_remotely("test") == True, 1
	assert check_word_meaning_remotely("mgr") == False, 2
	assert check_word_meaning_remotely("ouhgzoihg") == False, 3
	assert check_word_meaning_remotely("chicken") == True, 4
	
	# FIXME: apparently first need to create the file with "w" mode, and then open it for read/write
	mock_dict_file = open("unit_test_mock_file.txt", "w")
	mock_dict_file.close()
	mock_dict_file = open("unit_test_mock_file.txt", "r+")
	
	assert check_word_meaning_locally("test", dictionary_file=mock_dict_file) == False, 5
	assert check_word_meaning_locally("manager", dictionary_file=mock_dict_file) == False, 6
	
	add_local_word("test", mock_dict_file)
	
	assert check_word_meaning_locally("test", dictionary_file=mock_dict_file) == True, 7
	
	assert check_word_meaning("something", dictionary_file=mock_dict_file) == True, 8
	assert check_word_meaning("function", dictionary_file=mock_dict_file) == True, 9
	assert check_word_meaning("nooooooo", dictionary_file=mock_dict_file) == False, 10
	assert check_word_meaning("table", dictionary_file=mock_dict_file) == True, 11
	
	mock_dict_file.close()
	os.remove("unit_test_mock_file.txt")
	
	print "ALL TESTS OK"