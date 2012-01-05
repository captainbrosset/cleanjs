import re

from data.functiondata import FunctionData

class FileInfoParser():
	
	FUNCTIONS_PATTERNS = ["function[\s]+([a-zA-Z0-9_$]+)[\s]*\(([a-zA-Z0-9,\s]*)\)[\s]*\{",
						"([a-zA-Z0-9_$]+)[\s]*=[\s]*function[\s]*\(([a-zA-Z0-9,\s]*)\)[\s]*\{",
						"([a-zA-Z0-9_$]+)[\s]*:[\s]*function[\s]*\(([a-zA-Z0-9,\s]*)\)[\s]*\{"]
	SIGNATURE_PATTERN = "[a-zA-Z0-9_$]+"
	FUNCTIONS_BODY_PROCESSOR_SEP = "[[FUNCTIONSTART]]"
	VARIABLES_PATTERN = "var[\s]+([a-zA-Z0-9_$]+)"
		
	def _parse_signature(self, src):
		return re.findall(FileInfoParser.SIGNATURE_PATTERN, src)
	
	def _parse_bodies(self, src, pattern):
		# FIXME: the parser fails to understand nested functions (a function inside another function)
		bodies = []
		processed_src = re.sub(pattern, FileInfoParser.FUNCTIONS_BODY_PROCESSOR_SEP, src)
		src_split_by_first_occurence = processed_src.split(FileInfoParser.FUNCTIONS_BODY_PROCESSOR_SEP, 1)
		
		if len(src_split_by_first_occurence) > 1:
			processed_src = src_split_by_first_occurence[1]
			unprocessed_bodies = processed_src.split(FileInfoParser.FUNCTIONS_BODY_PROCESSOR_SEP)
		
			for body in unprocessed_bodies:
				opened_curly_brace = 0
				content = ""
				for char in body:
					# closing the function
					if char == "}" and opened_curly_brace == 0:
						break
					# closing an already opened brace
					if char == "}" and opened_curly_brace > 0:
						opened_curly_brace -= 1
					if char == "{":
						opened_curly_brace += 1
					content += char
				bodies.append(content)
		
		return bodies
		
	def parse_functions(self, src):
		functions = []
		
		for pattern in FileInfoParser.FUNCTIONS_PATTERNS:
			functions_bodies = self._parse_bodies(src, pattern)
			functions_signatures = re.finditer(pattern, src)
			for index, function_match in enumerate(functions_signatures):
				name = function_match.group(1)
				signature = self._parse_signature(function_match.group(2))
				body = functions_bodies[index]
				line_nb = src[0:function_match.start()].count("\n") + 1
				function = FunctionData(name, signature, body, line_nb)
				functions.append(function)

		return functions
	
	def parse_variables(self, src):
		return re.findall(FileInfoParser.VARIABLES_PATTERN, src)
	
	def parse_lines(self, src):
		return re.findall("^(.*)$", src, flags=re.MULTILINE);