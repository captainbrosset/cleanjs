from syntaxutils import jsparser

class Reviewer():
	def get_name(self):
		return "syntax"

	def extract_error_msg(self, jsparser_error):
		return jsparser_error.message.split("\n")[0]
	
	def extract_error_line(self, jsparser_error):
		return str(jsparser_error.message.split("\n")[1].split(":")[1])

	def review(self, file_data, message_bag):
		try:
			ast = jsparser.parse(file_data.content)
		except jsparser.ParseError as jsparser_error:
			message_bag.add_error(self, self.extract_error_msg(jsparser_error), self.extract_error_line(jsparser_error))
		
		
if __name__ == "__main__":
	class MockMessageBag(object):
		def __init__(self):
			self.errors = []
			self.line = ""
		def add_error(self, reviewer, message, line=None):
			self.errors.append(message)
			self.line = line
	
	class MockFileData(object):
		def __init__(self, content):
			self.content = content
	
	file_data = MockFileData("var a = 1; a ++;alert(a)")
	message_bag = MockMessageBag()
	reviewer = Reviewer()
	reviewer.review(file_data, message_bag)

	assert len(message_bag.errors) == 0, "Syntax error should not have been reported"

	file_data = MockFileData("""
		var a=0;
		if(test {
			return a;
		}
	""")

	message_bag.errors = []
	reviewer.review(file_data, message_bag)

	assert len(message_bag.errors) == 1, "Syntax error should have been reported"
	assert message_bag.line == "3", "Syntax error reported on the wrong line"

	print "ALL TESTS OK " + __file__