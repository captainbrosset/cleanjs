def output_messages(messages):
	"""
	Output messages to an HTML display
	"""
	report = "<ul>"
	
	for message in messages:
		report += "<li>"
		report += "<span class='type'>" + message.reviewer + " " + message.type + "</span>"
		if message.line:
			header += "<span class='line'>line " + str(message.line) + "</span>"
		report += "<span class='content'>" + message.content + "</span>"
		report += "</li>"
	
	report += "</ul>"
	
	return report