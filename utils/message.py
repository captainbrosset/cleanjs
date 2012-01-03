class MessageBag:
	def __init__(self):
		self.messages = []
		
	def add_warning(self, reviewer, content, line = None):
		self.messages.append(Message(Message.TYPE_WARNING, reviewer, content, line))
		
	def add_error(self, reviewer, content, line = None):
		self.messages.append(Message(Message.TYPE_ERROR, reviewer, content, line))
		
	def add_info(self, reviewer, content, line = None):
		self.messages.append(Message(Message.TYPE_INFO, reviewer, content, line))
	
	def _get_message_report_header(self, message):
		header = ""
		header += message.reviewer.get_name() + " " + message.type
		if message.line:
			header += ", line " + str(message.line)
		header += " | "
		return header
	
	def _get_report_pre_border(self, length):
		str = ""
		str += "+"
		str += "".join(["-" for i in range(length-2)])
		str += "+"
		return str
		
	def _get_report_post_border(self, length):
		str = ""
		str += "".join(["-" for i in range(length+1)])
		str += "+"
		return str
	
	def report_messages(self):
		report = "\n\n"
		
		# Pre-process all messages to know the max header size
		headers = []
		contents = []
		max_header_length = 0
		max_content_length = 0
		for message in self.messages:
			header_str = self._get_message_report_header(message)
			headers.append(header_str)
			contents.append(message.content)
			if len(header_str) > max_header_length:
				max_header_length = len(header_str)
			if len(message.content) > max_content_length:
				max_content_length = len(message.content)
		
		report += self._get_report_pre_border(max_header_length)
		report += self._get_report_post_border(max_content_length)
		report += "\n"
		
		# Now output messages
		for index, message in enumerate(self.messages):
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
			report += self._get_report_pre_border(max_header_length)
			report += self._get_report_post_border(max_content_length)
			report += "\n"
		
		report += "\n"
		
		return report
	
class Message:
	TYPE_WARNING = "warning"
	TYPE_INFO = "info"
	TYPE_ERROR = "error"
	
	def __init__(self, type, reviewer, content, line):
		self.type = type
		self.reviewer = reviewer
		self.content = content
		self.line = line