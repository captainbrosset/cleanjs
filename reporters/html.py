def output_messages(message_bag, file_data):
	"""
	Output messages to an HTML display
	"""
	messages = message_bag.get_messages()
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


if __name__ == "__main__":
	print "NO TESTS TO RUN " + __file__