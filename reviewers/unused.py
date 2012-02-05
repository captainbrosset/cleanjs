import re

class Reviewer():
	def get_name(self):
		return "unused"
	
	def escape_identifier_for_regexp(self, name):
		return name.replace("$", "\$")

	def get_regexp_to_find_identifier_usage(self, name):
		name = self.escape_identifier_for_regexp(name)
		
		before_identifier = "(?:^|[\s\[\]\(\)\+\-\{\};:,!]{1})"
		after_identifier = "(?:[\s\[\]\(\)\.\+\-\{\};:,]{1}|$)"

		return before_identifier + "(" + name + ")" + after_identifier
	
	def find_identifier_occurences(self, name, code):
		pattern = self.get_regexp_to_find_identifier_usage(name)
		return re.findall(pattern, code)

	def review_unused_arguments_in_functions(self, functions, message_bag):
		for function in functions:
			for argument in function.signature:
				occurences = self.find_identifier_occurences(argument, function.lines.get_whole_code())

				if len(occurences) == 0:
					message_bag.add_error(self, "Argument " + argument + " in method " + function.name + " is never used", function.line_number)
	
	def review_unused_variables_in_functions(self, functions, message_bag):
		for function in functions:
			for var in function.variables:
				occurences = self.find_identifier_occurences(var.name, function.lines.get_whole_code())

				if len(occurences) == 1:
					message_bag.add_error(self, "Variable " + var.name + " in method " + function.name + " is declared but never used", var.line_number)
	
	def review_ununsed_class_properties(self, class_properties, lines, message_bag):
		for property in class_properties:
			occurences = []
			name = self.escape_identifier_for_regexp(property.name)
			for line in lines:
				occurences += re.findall("this\." + name + "[\s]*[=\(\]\)\.;$\+]{1}", line.code)
			if len(occurences) == 1:
				message_bag.add_error(self, "Class property " + property.name + " is initialized but never used", property.line_number)

	def review(self, file_data, message_bag):
		self.review_unused_variables_in_functions(file_data.functions, message_bag)
		self.review_unused_arguments_in_functions(file_data.functions, message_bag)
		self.review_ununsed_class_properties(file_data.class_properties, file_data.lines.all_lines, message_bag)


if __name__ == "__main__":
	reviewer = Reviewer()

	assert len(reviewer.find_identifier_occurences("test", """
	var a = 2;
	thisisatest;
	""")) == 0

	assert len(reviewer.find_identifier_occurences("test", """
	test
	""")) == 1

	assert len(reviewer.find_identifier_occurences("test", """
	if(test) {
		test = 2;
		test(a)
	} else if (  test != 5) {
		setTest(test);
		this.test = test;
	}
	window[test] = 4
	test+=1;
	""")) == 8

	assert len(reviewer.find_identifier_occurences("test", """test""")) == 1

	assert len(reviewer.find_identifier_occurences("someBoolean", """
	if (!someBoolean) {
		//do stuff
	}
	""")) == 1

	print "ALL TESTS OK"