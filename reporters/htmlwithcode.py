def output_messages(message_bag, file_data):
	src_file_name = get_friendly_file_name(file_data.name)
	report_file_name = src_file_name + "-report.html"	
	report_file = open(report_file_name, "w")
	
	output_header(file_data.name, report_file)
	output_general_messages(message_bag, file_data.lines.total_lines, report_file)
	output_code_lines_messages(message_bag, file_data.lines.total_lines, report_file)
	output_footer(report_file)
	
	report_file.close()

def get_friendly_file_name(complete_name):
	last_slash = complete_name.rfind("/")
	src_file_name = complete_name

	if last_slash != -1:
		src_file_name = src_file_name[last_slash+1:]
	
	return src_file_name

def output_header(file_name, file_writer):
	file_writer.write("""<!DOCTYPE html>
	<html lang="en">
		<head>
			<meta charset="utf-8">
		    <title>cleanjs report for file """ + file_name + """</title>
			<style type="text/css">
				body {
					margin: 0;
					padding: 1em;
					font-size: 14px;
					font-family: 'Palatino Linotype', 'Book Antiqua', Palatino, FreeSerif, serif;
					overflow-x: hidden;
					width: 100%;
				}
				h1 {
					margin: 0;
					padding: 1em 1em 1em 25px;
				}
				.general {
					padding: 0;
					margin: 0 0 0 30px;
					list-style-type: none;
					width: 500px;
					padding: 1em;
					background: #eee;
					border-right: 1px solid #ccc;
					border-left: 1px solid #ccc;
					color: #333;
				}
				.general li {
					padding-bottom: 5px;
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
					padding-right: 5px;
					color: #aaa;
					font-family: Menlo, Monaco, Consolas, "Lucida Console", monospace;
					font-size: 11px;
				}
				.lines .line .messages {
					float: left;
					padding: 0 1em;
					margin: 0;
					list-style-type: none;
					width: 500px;
					border-right: 1px solid #ccc;
					border-left: 1px solid #ccc;
					background: #eee;
					color: #333;
				}
				.lines .line .messages li {
					padding-bottom: 8px;
					line-height: 13px;
				}
				.lines .line .code {
					float :left;
					margin: 0;
					padding: 0 1em;
					font-family: Menlo, Monaco, Consolas, "Lucida Console", monospace;
					font-size: 11px;
				}
				.error {
					color: #954121;
					color: red;
				}
				.info {
					
				}
				.warning {
					color: #B62;
				}
			</style>
		</head>
		<body>
			<h1>""" + file_name + """</h1>""")

def output_general_messages(message_bag, all_lines, file_writer):
	file_writer.write("<ul class='general'>")
	for message in message_bag.get_messages():
		if not message.line:
			file_writer.write("<li class='" + message.type + "'>" + message.content + "</li>")
	file_writer.write("</ul>")

def output_code_lines_messages(message_bag, all_lines, file_writer):
	file_writer.write("<ul class='lines'>")
	
	for index, line in enumerate(all_lines):
		file_writer.write("<li class='line'>")
		file_writer.write("<span class='gutter'>" + str(index + 1) + "</span>")
		file_writer.write("<ul class='messages'>")
		line_messages = message_bag.get_messages_on_line(index+1)
		if len(line_messages) == 0:
			file_writer.write("<li>&nbsp;</li>")
		for line_message in line_messages:
			file_writer.write("<li class='" + line_message.type + "'>" + line_message.content + "</li>")
		file_writer.write("</ul>")
		file_writer.write("<pre class='code'>" + html_escape(line) + "</pre>")
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