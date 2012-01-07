def output_messages(message_bag, file_data):
	last_slash = file_data.name.rfind("/")
	src_file_name = file_data.name

	if last_slash != -1:
		src_file_name = src_file_name[last_slash+1:]
	
	report_file_name = src_file_name + "-report.html"	
	report_file = open(report_file_name, "w")
	
	report_file.write("""<!DOCTYPE html>
	<html lang="en">
		<head>
			<meta charset="utf-8">
		    <title>cleanjs report for file """ + file_data.name + """</title>
			<style type="text/css">
				body {
					margin: 0;
					padding: 2em;
					font-family: arial;
					font-size: 1.1em;
				}
				h1 {
					margin: 0;
				}
				.code {
					background: #eee;
				}
				pre {
					margin: 0;
					font-size: 11px;
					color: #aaa;
				}
				pre span {
					border-left: 1px solid #aaa;
					color: black;
					padding-left: 10px;
				}
				div.msg {
					background: white;
					font-size: 11px;
					font-family: courier;
					margin: 2px 10px;
				}
				div.msg span {
					font-weight: bold;
				}
				div.error span {
					color: #D2344F;
				}
				div.info span {
					color: blue;
				}
				div.warning span {
					color: #F50;
				}
			</style>
		</head>
		<body>""")
	
	nb_of_total_lines = len(file_data.lines.total_lines)
	
	report_file.write("<h1>File: " + file_data.name + "</h1>")	
	report_file.write("<div class='code'>")
	
	for message in message_bag.get_messages():
		if not message.line:
			report_file.write("<div class='msg " + message.type + "'>" + _get_message_line_gutter(nb_of_total_lines) + "<span>" + message.reviewer + " " + message.type + ": " + message.content + "</span></div>")
	
	for index, line in enumerate(file_data.lines.total_lines):
		report_file.write("<pre>" + _get_line_number_gutter(index, nb_of_total_lines) + "<span>" + html_escape(line) + "</span></pre>")
		line_messages = message_bag.get_messages_on_line(index+1)
		for line_message in line_messages:
			report_file.write("<div class='msg " + line_message.type + "'>" + _get_message_line_gutter(nb_of_total_lines) + "<span>" + line_message.reviewer + " " + line_message.type + ": " + line_message.content + "</span></div>")
	
	report_file.write("</div></body></html>")	
	report_file.close()

def _get_line_number_gutter(index, total_nb):
	number = index + 1
	number_str = str(number)
	total_lines_char_nb = len(str(total_nb))
	current_line_char_nb = len(number_str)

	if current_line_char_nb < total_lines_char_nb:
		padding = "".join([" " for i in range(total_lines_char_nb - current_line_char_nb)])
		number_str = padding + number_str
		
	return number_str + "  "
	
def _get_message_line_gutter(total_nb):
	total_lines_char_nb = len(str(total_nb))
	padding = "".join([" " for i in range(total_lines_char_nb)])
	return padding + "  "

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