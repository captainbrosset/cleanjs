class InMemoryFile():
	def __init__(self):
		self.content = ""
	def write(self, str):
		self.content += str

def output_messages(result, file_data, to_file=None):
	message_bag = result["message_bag"]
	rating = result["rating"]

	report_file = None
	
	if to_file:
		report_file = open(to_file, "w")
	else:
		report_file = InMemoryFile()
	
	output_header(file_data.name, rating, report_file)
	output_general_messages(message_bag, report_file)
	output_code_lines_messages(message_bag, file_data.lines.all_lines, report_file)
	output_footer(report_file)
	
	if to_file:
		report_file.close()
		return None
	else:
		return report_file.content

def get_friendly_file_name(complete_name):
	last_slash = complete_name.rfind("/")
	src_file_name = complete_name

	if last_slash != -1:
		src_file_name = src_file_name[last_slash+1:]
	
	return src_file_name

def output_header(file_name, rating, file_writer):
	file_writer.write("""<!DOCTYPE html>
	<html lang="en">
		<head>
			<meta charset="utf-8">
		    <title>cleanjs report for file """ + file_name + """</title>
			<style type="text/css">
				body {
					margin: 0;
					padding: 1em;
					font-size: 12px;
					font-family: verdana;
					overflow-x: hidden;
					width: 100%;
					color: #444;
				}
				h1 {
					margin: 0;
					padding: 1em 1em 1em 25px;
				}
				.general {
					padding: 0;
					margin: 0 0 30px 30px;
					list-style-type: none;
					width: 500px;
					color: #222;
				}
				.lines {
					padding: 0;
					margin: 0;
					list-style-type: none;
					width: 10000px;
				}
				.lines .line {
					overflow: hidden;
					padding: 0;
					margin: 0;
					list-style-type: none;
				}
				.lines .line .gutter {
					float: left;
					text-align: right;
					width: 25px;
					padding: 4px 5px 4px 0;
					color: #aaa;
					font-size: 11px;
				}
				.lines .nomessage .gutter {
					color: #ddd;
				}
				.lines .line .messages {
					float: left;
					padding: 0;
					margin: 0;
					list-style-type: none;
					width: 500px;
				}
				.lines .line .messages li, .general li {
					padding: 4px 1em;
					line-height: 13px;
				}
				.lines .line .code {
					float :left;
					margin: 0;
					padding: 0 1em;
					font-family: Menlo, Monaco, Consolas, "Lucida Console", monospace;
					font-size: 11px;
				}
				.error, .info, .warning {
					border-left: 4px solid #3e93bf;
					background: #eee;
				}
				.warning {
					border-color: #f5931f;
				}
				.error {
					font-weight: bold;
					border-color: #d83e0f;
				}
			</style>
		</head>
		<body>
			<h1>""" + file_name + """ | grade """ + rating + """</h1>""")

def output_general_messages(message_bag, file_writer):
	file_writer.write("<ul class='general'>")
	for message in message_bag.get_messages():
		if not message.line:
			file_writer.write("<li class='" + message.type + "'>" + message.content + "</li>")
	file_writer.write("</ul>")

def output_code_lines_messages(message_bag, all_lines, file_writer):
	file_writer.write("<ul class='lines'>")
	
	for line in all_lines:
		line_messages = message_bag.get_messages_on_line(line.line_number)
		nb_line_messages = len(line_messages)
		
		line_class = "line"
		if nb_line_messages == 0:
			line_class += " nomessage"
		
		file_writer.write("<li class='" + line_class + "'>")
		file_writer.write("<span class='gutter'>")
		file_writer.write(str(line.line_number))
		file_writer.write("</span>")
		file_writer.write("<ul class='messages'>")
		
		if nb_line_messages == 0:
			file_writer.write("<li>&nbsp;</li>")
			
		for line_message in line_messages:
			file_writer.write("<li class='" + line_message.type + "'>" + line_message.content + "</li>")
			
		file_writer.write("</ul>")
		file_writer.write("<pre class='code'>" + html_escape(line.complete_line) + "</pre>")
		file_writer.write("</li>")
			
	file_writer.write("</ul>")

def output_footer(file_writer):
	file_writer.write("</body></html>")
	
html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;",
    }

def html_escape(text):
    """Produce entities within text."""
    return "".join(html_escape_table.get(c,c) for c in text)


if __name__ == "__main__":
	print "NO TESTS TO RUN " + __file__