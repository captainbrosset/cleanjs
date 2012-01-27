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
		return sorted(self.messages, key=lambda message: message.line)

	def get_messages_on_line(self, line_nb):
		messages = []
		for message in self.messages:
			if message.line == line_nb:
				messages.append(message)
		return messages

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
	
	def __repr__(self):
		return self.reviewer + " " + self.type + " line " + str(self.line) + " : " + self.content


if __name__ == "__main__":
	
	class MockReviewer():
		def get_name(self):
			return "mock"
	
	bag = MessageBag()
	
	bag.add_warning(MockReviewer(), "warning 1", 1)
	bag.add_warning(MockReviewer(), "warning 2", 2)
	bag.add_warning(MockReviewer(), "warning 3", 3)
	
	bag.add_error(MockReviewer(), "error 1", 1)
	bag.add_error(MockReviewer(), "error 2", 2)
	bag.add_error(MockReviewer(), "error 3", 3)
	
	bag.add_info(MockReviewer(), "info 1", 1)
	bag.add_info(MockReviewer(), "info 2", 2)
	bag.add_info(MockReviewer(), "info 3", 3)
	
	all_messages = bag.get_messages()
	assert len(all_messages) == 9, 1
	assert all_messages[0].line == 1
	assert all_messages[3].line == 2
	assert all_messages[6].line == 3
	
	messages_on_line_2 = bag.get_messages_on_line(2)
	assert len(messages_on_line_2) == 3
	assert messages_on_line_2[0].line == 2
	
	bag.reset_messages()
	assert len(bag.get_messages()) == 0
	
	print "ALL TESTS OK"