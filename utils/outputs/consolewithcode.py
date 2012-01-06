def output_messages(message_bag, file_data):
	print "========================"
	print "File: " + file_data.name
	print "========================"
	
	print "General comments:"
	for message in message_bag.get_messages():
		if not message.line:
			print "- " + message.content
	
	print "========================"
	print "Code"
	print "========================"
	
	for index, line in enumerate(file_data.lines.total_lines):
		print _get_line_number_gutter(index) + line
		line_messages = message_bag.get_messages_on_line(index+1)
		for line_message in line_messages:
			print "   | >> " + line_message.reviewer + " " + line_message.type + ": " + line_message.content

def _get_line_number_gutter(index):
	number = index + 1
	number_str = str(number)
	if number < 10:
		number_str = "0" + str(number)
	
	return number_str + " | "