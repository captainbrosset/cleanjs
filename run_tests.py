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

def output_integration_test_errors(actual, expected):
	if len(expected) != len(actual):
		print "Actual results length don't match expected results length"
	
	for key, item in actual.iteritems():
		if expected[key]["rating"] != item["rating"]:
			print "Rating of " + key + " is incorrect, expected " + expected[key]["rating"] + ", found " + item["rating"]
		if item["messages"] != expected[key]["messages"]:
			print "Messages of " + key + " are incorrect, expected:\n" + str(expected[key]["messages"]).replace("},","\n")
			print "found:\n" + str(item["messages"]).replace("},","\n")

def run_integration_tests():
	script_dir = "testscripts"
	report_dir = script_dir + os.sep + "reports"
	ensure_dir(report_dir)

	from testscripts import expected
	expected_results = expected.results
	actual_results = {}
	
	for item in os.listdir(script_dir):
		if item[-3:] == ".js":
			# Gather data about the file to be reviewed
			from parsers import fileparser
			file_data = fileparser.get_file_data_from_file(script_dir + os.sep + item)

			# Review the file
			from reviewers import reviewer
			result = reviewer.review(file_data)

			rating = result["rating"]
			messages = result["message_bag"].get_messages()
			
			actual_results[item] = {
				"rating": rating,
				"messages": []
			}
			for m in messages:
				actual_results[item]["messages"].append({
					"type": m.type,
					"reviewer": m.reviewer,
					"line": m.line
				})

	if expected_results != actual_results:
		output_integration_test_errors(actual_results, expected_results)
		assert True == False, "Integration tests did not output the same number or type of messages"
	
	print "ALL FILES OK"

print ""
print "-- RUNNING ALL UNIT TESTS"
run_unit_tests(".")

print ""
print "-- RUNNING ALL INTEGRATION TESTS"
run_integration_tests()