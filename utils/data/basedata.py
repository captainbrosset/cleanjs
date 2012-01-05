import re

class BaseData:
	def find_line_numbers_in_content(self, content, pattern, flags=None):
		results = []
		# FIXME: make this better
		if flags:
			matches = re.finditer(pattern, content, flags=flags)
		else:
			matches = re.finditer(pattern, content)
		for match in matches:
			result = BaseData.LineNumberMatchObject(content[0:match.start()].count("\n") + 1, match)
			results.append(result)
		return results
	
	class LineNumberMatchObject:
		def __init__(self, line_number, match_object):
			self.line_number = line_number
			self.match_object = match_object