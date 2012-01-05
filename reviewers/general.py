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
			function_length = len(re.findall("^.*\S+.*$", function.body, flags=re.MULTILINE))
			average += function_length
			if function_length > max:
				max = function_length
			elif function_length < min:
				min = function_length
		average = average / len(functions)
		message_bag.add_info(self, "Longest function is " + str(max) + " lines long, and shortest one is " + str(min) + " (average is " + str(average) + ")")

	def review_todos_and_fixmes(self, file_data, message_bag):
		matches = file_data.find_line_numbers("FIXME|TODO")
		for match in matches:
			message_bag.add_info(self, "Line has TODO or FIXME flag", match.line_number)

	def review(self, file_data, message_bag):
		message_bag.add_info(self, "File is " + str(len(file_data.lines)) + " lines long")
		message_bag.add_info(self, "There are " + str(len(file_data.functions)) + " functions in the file")
		self.review_min_max_function_length(file_data.functions, message_bag)
		self.review_todos_and_fixmes(file_data, message_bag)