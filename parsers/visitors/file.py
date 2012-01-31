import re

import visitor

class LineData:
	"""Data structure holding structured information about a piece of source code.
	Instances of this class have the following attributes:
	- code_lines: an array of all the lines of pure code (no comments), striped from white spaces
	- comment_lines: an array of all the lines of comments (no code), striped from white spaces
	- empty_lines: an array of all empty lines
	- total_lines: an array of all lines"""
	
	def __init__(self, code_lines, comment_lines, empty_lines, total_lines):
		self.code_lines = code_lines
		self.comment_lines = comment_lines
		self.empty_lines = empty_lines
		self.total_lines = total_lines
		
class File(visitor.Entity):
	"""Represents the file itself.
	- content: the source code
	- line_data: an instance of LineData"""
	
	def __init__(self, content, line_data):
		super(File, self).__init__(0, 0, len(content))
		
		self.content = content
		self.line_data = line_data

class FileVisitor:
	"""File visitor implementation.
	
	Only implements the FILECONTENT event listener to get the complete
	source code of the file."""

	def __init__(self):
		self.entities = []

	def parse_total_lines(self, src):
		return re.findall("^(.*)$", src, flags=re.MULTILINE);
		
	def differentiate_empty_nonempty_lines(self, total_lines):
		empty_lines = []
		nonempty_lines = []
		for line in total_lines:
			if self.is_empty_line(line):
				empty_lines.append(line)
			else:
				nonempty_lines.append(line)
		return {
			"empty_lines": empty_lines,
			"nonempty_lines": nonempty_lines
		}
	
	def is_empty_line(self, line):
		return len(re.findall("^\s*$", line)) != 0
	
	def parse_comments_and_code_lines(self, file_content):
		comments = ""
		code = ""
		inside_multi_comment = False
		inside_comment = False
		skip = False
		
		code_to_add = ""
		comments_to_add = ""

		for index, char in enumerate(file_content):
			if skip:
				skip = False
				continue
			
			if char == "\n":
				if inside_comment:
					inside_comment = False
					comments += "\n"
			
			if char == "/" and not inside_comment and file_content[index+1:index+2] == "*":
				inside_multi_comment = True
				comments_to_add = char + "*"
				skip = True
			elif char == "/" and not inside_comment and file_content[index+1:index+2] == "/":
				inside_comment = True
				comments_to_add = char + "/"
				skip = True
			elif inside_multi_comment and char == "*" and file_content[index+1:index+2] == "/":
				comments += char + "/"
				skip = True
				inside_multi_comment = False
				comments += "\n"
			elif not inside_comment and not inside_multi_comment:
				code_to_add = char
			else:
				comments_to_add = char
			
			comments += comments_to_add
			code += code_to_add
			
			comments_to_add = ""
			code_to_add = ""
		
		comments = re.sub("^[\s]*|[\s]*$", "", comments, flags=re.MULTILINE)
		comment_lines = self.parse_total_lines(comments)
		comment_lines = self.differentiate_empty_nonempty_lines(comment_lines)["nonempty_lines"]
		
		code = re.sub("^[\s]*|[\s]*$", "", code, flags=re.MULTILINE)
		code_lines = self.parse_total_lines(code)
		code_lines = self.differentiate_empty_nonempty_lines(code_lines)["nonempty_lines"]
		
		return {
			"comment_lines": comment_lines,
			"code_lines": code_lines
		}
	
	def parse_lines(self, src):
		total_lines = self.parse_total_lines(src)
		sorted_lines = self.differentiate_empty_nonempty_lines(total_lines)
		empty_lines = sorted_lines["empty_lines"]
		comments_and_code = self.parse_comments_and_code_lines("\n".join(sorted_lines["nonempty_lines"]))
		comment_lines = comments_and_code["comment_lines"]
		code_lines = comments_and_code["code_lines"]

		return LineData(code_lines, comment_lines, empty_lines, total_lines)
		
	def visit_FILECONTENT(self, source):
		line_data = self.parse_lines(source)
		self.entities.append(File(source, line_data))