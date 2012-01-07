import re

class LineData:
	"""
	Data structure holding structured information about a piece of source code.
	Instances of this class have the following attributes:
	- code_lines: an array of all the lines of pure code (no comments), striped from white spaces
	- comment_lines: an array of all the lines of comments (no code), striped from white spaces
	- empty_lines: an array of all empty lines
	- total_lines: an array of all lines
	"""
	def __init__(self, code_lines, comment_lines, empty_lines, total_lines):
		self.code_lines = code_lines
		self.comment_lines = comment_lines
		self.empty_lines = empty_lines
		self.total_lines = total_lines

class LineParser():
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
	
	def parse(self, src):
		total_lines = self.parse_total_lines(src)
		sorted_lines = self.differentiate_empty_nonempty_lines(total_lines)
		empty_lines = sorted_lines["empty_lines"]
		comments_and_code = self.parse_comments_and_code_lines("\n".join(sorted_lines["nonempty_lines"]))
		comment_lines = comments_and_code["comment_lines"]
		code_lines = comments_and_code["code_lines"]

		return LineData(code_lines, comment_lines, empty_lines, total_lines)


if __name__ == "__main__":
	parser = LineParser()
		
	assert parser.is_empty_line("") == True, 11
	assert parser.is_empty_line("     ") == True, 12
	assert parser.is_empty_line("			   ") == True, 13
	assert parser.is_empty_line("	  	") == True, 14
	assert parser.is_empty_line("	};  	") == False, 15
	assert parser.is_empty_line("};") == False, 16
	
	file_content = """/**
	 * This is a test class
	 * @param {String} test
	 */
	my.package.Class = function() {
		// This function does something
		var a = 1;
		
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
	
	line_data = parser.parse(file_content)
	
	assert len(line_data.total_lines) == 24, "total number of lines is incorrect. Expected 24, found " + str(len(line_data.total_lines))
	assert len(line_data.empty_lines) == 2, "number of empty lines is incorrect. Expected 2, found " + str(len(line_data.empty_lines))
	assert len(line_data.code_lines) == 9, "number of lines of code is incorrect. Expected 9, found " + str(len(line_data.code_lines))
	assert len(line_data.comment_lines) == 15, "number of lines of comments is incorrect. Expected 15, found " + str(len(line_data.comment_lines))
	
	print "ALL TESTS OK"