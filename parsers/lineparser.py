import re

class Line:
	"""A line object, containing its line_number, string of code if any, and string of comments if any"""
	
	def __init__(self, line_number, complete_line, code, comments):
		self.complete_line = complete_line
		self.line_number = line_number
		self.code = code
		self.comments = comments
	
	def __repr__(self):
		return "  - line " + str(self.line_number) + " | " + self.complete_line

	def is_empty(self):
		return self.code == "" and self.comments == ""
	
	def has_comments(self):
		return self.comments != ""
	
	def has_code(self):
		return self.code != ""
	
	def is_only_code(self):
		return self.code != "" and self.comments == ""
	
	def is_only_comments(self):
		return self.code == "" and self.comments != ""
	
	def is_both_code_and_comments(self):
		return self.code != "" and self.comments != ""

class LinesData:
	"""Data structure holding information about a piece of source code.
	Instances of this class have the following attribute:
	- all_lines: an array of all the lines in the file. Each element of this array is of type Line"""
	
	def __init__(self, all_lines):
		self.all_lines = all_lines
	
	def __repr__(self):
		return str(len(self.all_lines)) + " lines of code"

	def get_code_lines(self):
		lines = []
		for line in self.all_lines:
			if line.has_code():
				lines.append(line)
		return lines
		
	def get_comments_lines(self):
		lines = []
		for line in self.all_lines:
			if line.has_comments():
				lines.append(line)
		return lines

	def get_empty_lines(self):
		lines = []
		for line in self.all_lines:
			if line.is_empty():
				lines.append(line)
		return lines

class LineParser():
	"""Parse lines of code, lines of comments and empty lines from a source code"""
		
	def parse_lines(self, file_content, start_line_number=0):
		# FIXME: fails on the following case (consider the // as a comment start even inside a regexp):
		# pattern = /[0-9]+\//gi;

		all_lines = file_content.split("\n")
		lines = [{
			"code": "",
			"comments": ""
		}]
		line_index = 0;
		inside_multi_comment = False
		inside_comment = False
		inside_single_quoted_string = False
		inside_double_quoted_string = False
		skip = False
		code_to_add = ""
		comments_to_add = ""
				
		for index, char in enumerate(file_content):
			if char == "\n":
				lines.append({
					"code": "",
					"comments": ""
				})
				line_index += 1
			
			if skip:
				skip = False
				continue
						
			if char == "\n":
				if inside_comment:
					inside_comment = False
			
			if char == "'" and not inside_comment and not inside_single_quoted_string:
				inside_single_quoted_string = True
			elif char == "'" and not inside_comment and inside_single_quoted_string:
				inside_single_quoted_string = False
			
			if char == "\"" and not inside_comment and not inside_double_quoted_string:
				inside_double_quoted_string = True
			elif char == "\"" and not inside_comment and inside_double_quoted_string:
				inside_double_quoted_string = False

			if char == "/" and not inside_comment and file_content[index+1:index+2] == "*" and not inside_single_quoted_string and not inside_double_quoted_string:
				inside_multi_comment = True
				comments_to_add = char + "*"
				skip = True
			elif char == "/" and not inside_comment and file_content[index+1:index+2] == "/" and not inside_single_quoted_string and not inside_double_quoted_string:
				inside_comment = True
				comments_to_add = char + "/"
				skip = True
			elif inside_multi_comment and char == "*" and file_content[index+1:index+2] == "/":
				lines[line_index]["comments"] += char + "/"
				skip = True
				inside_multi_comment = False
			elif not inside_comment and not inside_multi_comment and char != "\n":
				code_to_add = char
			elif char != "\n":
				comments_to_add = char
			
			lines[line_index]["comments"] += comments_to_add
			lines[line_index]["code"] += code_to_add
			
			comments_to_add = ""
			code_to_add = ""

		line_objects = []
		for index, line in enumerate(lines):
			line_objects.append(Line(index+1+start_line_number, all_lines[index], line["code"].strip(), line["comments"].strip()))

		return line_objects
	
	def parse(self, src, start_line_number=0):
		all_lines = self.parse_lines(src, start_line_number)

		return LinesData(all_lines)


if __name__ == "__main__":
	
	parser = LineParser()
	
	file_content = """/**
	 * This is a test class
	 * @param {String} test
	 */
	my.package.Class = function() {
		// This function does something
		var a = 122;

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
			// Just simply return the field
			return this.someField; // And some inline comment
		}
	};"""
	
	lines_data = parser.parse(file_content)
	
	assert len(lines_data.all_lines) == 24, "total number of lines is incorrect. Expected 24, found " + str(len(lines_data.all_lines))
	assert len(lines_data.get_code_lines()) == 9, "total number of code lines is incorrect. Expected 9, found " + str(len(lines_data.get_code_lines()))
	assert len(lines_data.get_comments_lines()) == 15, "total number of comments lines is incorrect. Expected 15, found " + str(len(lines_data.get_comments_lines()))
	assert lines_data.get_code_lines()[4].code == "my.package.Class.prototype = {", "incorrect code line content extracted"
	assert lines_data.get_code_lines()[6].code == "return this.someField;", "incorrect code line content extracted"

	tricky_file_content = """var a = 1;
	a ++;
	// some function
	function some(yes) {
		var pattern = "http://a.url";
	}
	/* something tricky? */
	anotherthing = /[a-z]*\//g;"""

	lines_data = parser.parse(tricky_file_content)

	assert len(lines_data.all_lines) == 8, "total number of lines is incorrect. Expected 8, found " + str(len(lines_data.all_lines))
	assert len(lines_data.get_comments_lines()) == 2, "total number of comments lines is incorrect. Expected 2, found " + str(len(lines_data.get_comments_lines()))

	print "ALL TESTS OK " + __file__