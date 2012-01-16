import re

class Reviewer():
	def get_name(self):
		return "general"
		
	def get_help(self):
		return """Check general metrics and information about the file
		- FIXME and TODO comments
		- file length
		- number of functions
		- minimum and maximum function size"""

	def review_min_max_function_length(self, functions, message_bag):
		min = float("inf")
		max = 0
		average = 0
		for function in functions:
			# FIXME: need to take advantage of the new functions structured data to avoid parsing with the regexp here
			function_length = len(re.findall("^.*\S+.*$", function.body, flags=re.MULTILINE))
			average += function_length
			if function_length > max:
				max = function_length
			elif function_length < min:
				min = function_length
		if len(functions) != 0:
			average = average / len(functions)
		message_bag.add_info(self, "Longest function is " + str(max) + " lines long, and shortest one is " + str(min) + " (average is " + str(average) + ")")

	def review_todos_and_fixmes(self, file_data, message_bag):
		todo_matches = file_data.find_line_numbers("TODO(.*)")
		for match in todo_matches:
			message_bag.add_info(self, "TODO " + match.match_object.group(1), match.line_number)
			
		fixme_matches = file_data.find_line_numbers("FIXME(.*)")
		for match in fixme_matches:
			message_bag.add_info(self, "FIXME " + match.match_object.group(1), match.line_number)

	def review(self, file_data, message_bag):
		message_bag.add_info(self, "File is " + str(len(file_data.lines.all_lines)) + " lines long")
		message_bag.add_info(self, str(len(file_data.lines.get_comments_lines())) + " lines of comments")
		message_bag.add_info(self, str(len(file_data.lines.get_code_lines())) + " lines of code")
		message_bag.add_info(self, str(len(file_data.lines.get_empty_lines())) + " empty lines")
		message_bag.add_info(self, "There are " + str(len(file_data.functions)) + " functions in the file")
		self.review_min_max_function_length(file_data.functions, message_bag)
		self.review_todos_and_fixmes(file_data, message_bag)


if __name__ == "__main__":
	
	file_content = """
	/**
	 * This is a test class
	 * @param {String} test
	 */
	my.package.Class = function() {
		// This function does something
		var a = 1;
		
		// TODO: really implement this function
		
		/**
		 * some field
		 * @type {Boolean}
		 */
		this.someField = false; /* and some inline block comment */
	};
	
	my.package.Class.prototype = {
		/**
		 * Return the current value of the field
		 */
		getField : function() {
			// FIXME: there is something to be fixed here
			// Just simply return the field
			return this.someField; // And some inline comment
		}
	};
	"""
	
	# Tricking the PYTHONPATH because relative imports don't work when running the file standalone
	import sys
	sys.path.append("../")
	
	# Creating the reviewer instance, giving it the parsed file
	import fileparser
	file_data = fileparser.get_file_data_from_content("test_file", file_content)
	import messagebag
	message_bag = messagebag.MessageBag()
	reviewer = Reviewer()
	
	# Checking that 2 TODOFIXMES are found
	reviewer.review_todos_and_fixmes(file_data, message_bag)
	assert len(message_bag.get_messages()) == 2, 1
	assert message_bag.get_messages()[0].line == 10, 2
	assert message_bag.get_messages()[1].line == 24, 3
	message_bag.reset_messages()
	
	# Checking the fucntion stats
	reviewer.review_min_max_function_length(file_data.functions, message_bag)
	assert message_bag.messages[0].content == "Longest function is 8 lines long, and shortest one is 3 (average is 5)", 4
	
	print "ALL TESTS OK " + __file__