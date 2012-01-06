class MessageBag:
	def __init__(self):
		self.messages = []
		
	def add_warning(self, reviewer, content, line = None):
		self.messages.append(Message(Message.TYPE_WARNING, reviewer, content, line))
		
	def add_error(self, reviewer, content, line = None):
		self.messages.append(Message(Message.TYPE_ERROR, reviewer, content, line))
		
	def add_info(self, reviewer, content, line = None):
		self.messages.append(Message(Message.TYPE_INFO, reviewer, content, line))
	
	def get_messages(self):
		return self.messages

	def reset_messages(self):
		self.messages = []
	
class Message:
	TYPE_WARNING = "warning"
	TYPE_INFO = "info"
	TYPE_ERROR = "error"
	
	def __init__(self, type, reviewer, content, line):
		self.type = type
		self.reviewer = reviewer.get_name()
		self.content = content
		self.line = line