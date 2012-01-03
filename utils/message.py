class MessageBag:
    def __init__(self):
        self.messages = []
        
    def add_warning(self, reviewer, content):
        self.messages.append(Message(Message.TYPE_WARNING, reviewer, content))
        
    def add_error(self, reviewer, content):
        self.messages.append(Message(Message.TYPE_ERROR, reviewer, content))
        
    def add_info(self, reviewer, content):
        self.messages.append(Message(Message.TYPE_INFO, reviewer, content))
        
    def report_messages(self):
        report = ""
        for message in self.messages:
            report += message.report_message() + "\n"
        
        return report
    
class Message:
    TYPE_WARNING = "warning"
    TYPE_INFO = "info"
    TYPE_ERROR = "error"
    
    def __init__(self, type, reviewer, content):
        self.type = type
        self.reviewer = reviewer
        self.content = content
    
    def report_message(self):
        report = "[" + self.reviewer.get_name() + "] "
        report += "[" + self.type.upper() + "] "
        report += self.content
        return report