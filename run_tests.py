import os

def run_unit_tests(dir):
	for item in os.listdir(dir):
		if item[-3:] == ".py" and item[0:8] != "cleanjs_" and item != "run_tests.py" and item != "jsparser.py" and item[0:8] != "__init__":
			print "- " + os.path.join(dir, item)
			os.system("python " + os.path.join(dir, item))
		try:
			run_unit_tests(os.path.join(dir, item))
		except:
			pass

def ensure_dir(dir_name):
	if not os.path.exists(dir_name):
		os.makedirs(dir_name)

def get_list_of_messages_easy_to_compare(messages):
	easy_list = []
	for message in messages:
		if message.type != "info":
			easy_list.append(str(message.line) + " " + message.content)
	return sorted(easy_list)

def run_integration_tests():
	script_dir = "testscripts"
	report_dir = script_dir + os.sep + "reports"
	ensure_dir(report_dir)
	
	from parsers import fileparser
	from reviewers import reviewer
	
	from testscripts import expected
	expected_results = expected.results

	for item in os.listdir(script_dir):
		if item[-3:] == ".js":
			print "- " + item

			if not expected_results.has_key(item):
				print "seems to be a new file for which no reference data exist"
				continue

			# Gather data about the file to be reviewed
			file_data = None
			try:
				file_data = fileparser.get_file_data_from_file(script_dir + os.sep + item)
			except Exception as error:
				print error
				break;

			# Review the file
			result = reviewer.review(file_data)

			messages = get_list_of_messages_easy_to_compare(result.message_bag.get_messages())
			
			if not expected_results[item].has_key("messages") and messages != []:
				assert False, "Found messages for " + item + ", but none expected. Found:\n" + str(messages)
			elif expected_results[item].has_key("messages") and messages == []:
				assert False, "Expected messages for " + item + " but none found. Expected:\n" + str(expected_results[item]["messages"])
			elif expected_results[item].has_key("messages") and messages != []:
				assert sorted(expected_results[item]["messages"]) == messages, "incorrect messages found for " + item + " expected results not found:\n" + str(list(set(expected_results[item]["messages"]) - set(messages))) + "\nfound results not expected\n" + str(list(set(messages) - set(expected_results[item]["messages"])))
	
	print "ALL FILES OK"

if __name__ == "__main__":
	print ""
	print "-- RUNNING ALL UNIT TESTS"
	run_unit_tests(".")

	print ""
	print "-- RUNNING ALL INTEGRATION TESTS"
	run_integration_tests()