def output_messages(result, file_data):
	message_bag = result["message_bag"]
	
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
	
	nb_of_total_lines = len(file_data.lines.total_lines)
	
	for index, line in enumerate(file_data.lines.total_lines):
		print _get_line_number_gutter(index, nb_of_total_lines) + line
		line_messages = message_bag.get_messages_on_line(index+1)
		for line_message in line_messages:
			print _get_message_line_gutter(nb_of_total_lines) + line_message.reviewer + " " + line_message.type + ": " + line_message.content

def _get_line_number_gutter(index, total_nb):
	number = index + 1
	number_str = str(number)
	total_lines_char_nb = len(str(total_nb))
	current_line_char_nb = len(number_str)

	if current_line_char_nb < total_lines_char_nb:
		padding = "".join([" " for i in range(total_lines_char_nb - current_line_char_nb)])
		number_str = padding + number_str
		
	return number_str + " | "
	
def _get_message_line_gutter(total_nb):
	total_lines_char_nb = len(str(total_nb))
	padding = "".join([" " for i in range(total_lines_char_nb - 1)])
	return padding + "! | >> "


if __name__ == "__main__":
	print "NO TESTS TO RUN " + __file__