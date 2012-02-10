import ConfigParser

class ReviewerConfigReader(object):
	def __init__(self, cfg_file="messages.cfg"):
		self.config = ConfigParser.ConfigParser()
		self.config.read(cfg_file)

	def _replace_params(self, string, params):
		index = 1
		for param in params:
			string = string.replace("$" + str(index), str(param))
			index += 1
		return string

	def get(self, type, key, *params):
		string = self.config.get(type, key, "test")
		if params:
			string = self._replace_params(string, params)
		return string


if __name__ == "__main__":
	import os
	
	cfg_file = "messages.cfg"
	if __file__[0:2] == "./":
		cfg_file = "reviewers" + os.sep + "config" + os.sep + "messages.cfg"

	reader = ReviewerConfigReader(cfg_file)
	assert reader.get("codesize", "line_too_long", 120, 200) == "Line is more than 120 character long (200). This is hard to read."

	print "ALL TESTS OK"