class MessageBag:
	def __init__(self):
		self.messages = []
		
	def add_warning(self, reviewer, content, line = None):
		self.messages.append(Message(Message.TYPE_WARNING, reviewer, content, line))
		
	def add_error(self, reviewer, content, line = None):
		self.messages.append(Message(Message.TYPE_ERROR, reviewer, content, line))
		
	def add_info(self, reviewer, content, line = None):
		self.messages.append(Message(Message.TYPE_INFO, reviewer, content, line))
		
	def report_messages(self, src_file_name):
		report = ""
		for message in self.messages:
			report += "[" + src_file_name[src_file_name.rfind("/")+1:] + "]"
			report += message.report_message() + "\n"
		
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
	
	def report_message(self):
		report = "[" + self.reviewer.get_name() + " " + self.type + "]"
		if self.line:
			report += "[line " + str(self.line) + "]"
		report += " " + self.content
		return report