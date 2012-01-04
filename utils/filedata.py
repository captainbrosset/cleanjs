from parser import FileInfoParser

class FileData():
	"""A FileData instance is passed to reviewers"""
	def __init__(self, content, lines, functions, variables):
		self.content = content
		self.lines = lines
		self.functions = functions
		self.variables = variables

def get_file_data_from_content(src_file_content):
	"""Use this to gather data for file, given its content"""
	parser = FileInfoParser()
	src_file_functions = parser.parse_functions(src_file_content)
	src_file_variables = parser.parse_variables(src_file_content)
	src_file_lines = parser.parse_lines(src_file_content)

	return FileData(src_file_content, src_file_lines, src_file_functions, src_file_variables)

def get_file_data_from_file(src_file_name):
	"""Use this to gather data for file, given its path and name"""
	return get_file_data_from_content(open(src_file_name, 'r').read())
