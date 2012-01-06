def output_messages(message_bag, file_data):
	"""
	Output messages in the console, so in the simple text format, with some formatting
	"""
	messages = message_bag.get_messages()
	report = "\n\n"
	
	# Pre-process all messages to know the max header size
	headers = []
	contents = []
	max_header_length = 0
	max_content_length = 0
	for message in messages:
		header_str = _get_message_report_header(message)
		headers.append(header_str)
		contents.append(message.content)
		if len(header_str) > max_header_length:
			max_header_length = len(header_str)
		if len(message.content) > max_content_length:
			max_content_length = len(message.content)
	
	report += _get_report_pre_border(max_header_length)
	report += _get_report_post_border(max_content_length)
	report += "\n"
	
	# Now output messages
	for index, message in enumerate(messages):
		pre_padding_length = 0
		if len(headers[index]) < max_header_length:
			pre_padding_length = max_header_length - len(headers[index])
			
		post_padding_length = 0
		if len(contents[index]) < max_content_length:
			post_padding_length = max_content_length - len(contents[index])
		
		report += "|"
		report += "".join([" " for i in range(pre_padding_length)])
		report += headers[index]
		report += contents[index]
		report += "".join([" " for i in range(post_padding_length)])
		report += "|\n"
		report += _get_report_pre_border(max_header_length)
		report += _get_report_post_border(max_content_length)
		report += "\n"
	
	report += "\n"
	
	return report

def _get_message_report_header(message):
	header = ""
	header += message.reviewer + " " + message.type
	if message.line:
		header += ", line " + str(message.line)
	header += " | "
	return header

def _get_report_pre_border(length):
	str = ""
	str += "+"
	str += "".join(["-" for i in range(length-2)])
	str += "+"
	return str
	
def _get_report_post_border(length):
	str = ""
	str += "".join(["-" for i in range(length+1)])
	str += "+"
	return str