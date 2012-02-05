import codesize, comments, complexity, formatting, naming, unused, general
from messagebag import MessageBag

def review(file_data):
	"""Takes in a FileData instance, runs all reviewers on it, and returns a reviewers.reviewer.ReviewedFile instance"""

	message_bag = MessageBag()

	general.Reviewer().review(file_data, message_bag)
	codesize.Reviewer().review(file_data, message_bag)
	comments.Reviewer().review(file_data, message_bag)
	complexity.Reviewer().review(file_data, message_bag)
	formatting.Reviewer().review(file_data, message_bag)
	naming.Reviewer().review(file_data, message_bag)
	unused.Reviewer().review(file_data, message_bag)

	return ReviewedFile(message_bag)

class ReviewedFile(object):
	"""
	Instances of this class result from the review of a file.
	Available properties are:
	- message_bag: An instance of reviewers.messagebag.MessageBag
	- rate: A string that indicates the rate of the file according to the number of problems the reviewers found.
	"""

	RATES = ["A+","A","A-","B+","B","B-","C+","C","C-","D+","D","D-","E+","E","E-","F+","F","F-"]

	def __init__(self, message_bag):
		self.message_bag = message_bag
		self.rate = self.get_rate_mark()

	def get_rate_number(self):
		nb_warnings = 0
		nb_errors = 0

		for msg in self.message_bag.get_messages():
			if msg.type == "warning":
				nb_warnings += 1
			if msg.type == "error":
				nb_errors += 1

		# errors are 3 times more important than warnings
		total_nb_of_msgs = int(round(float(nb_errors * 3 + nb_warnings) / 3))
		if total_nb_of_msgs > 17:
			total_nb_of_msgs = 17

		return total_nb_of_msgs
	
	def get_rate_mark(self):
		rating = ReviewedFile.RATES[self.get_rate_number()]

		return rating

if __name__ == "__main__":

	class MockMessage(object):
		def __init__(self, type):
			self.type = type
	
	class MockBag(object):
		def __init__(self, messages):
			self.messages = messages
		def get_messages(self):
			return self.messages
	
	msg_warning = MockMessage("warning")
	msg_error = MockMessage("error")
	
	assert ReviewedFile(MockBag([msg_warning,msg_warning,msg_warning,msg_warning,msg_warning])).rate == "A-"
	assert ReviewedFile(MockBag([msg_error,msg_error,msg_error,msg_error])).rate == "B"
	assert ReviewedFile(MockBag([])).rate == "A+"
	assert ReviewedFile(MockBag([msg_error, msg_error, msg_warning])).rate == "A-"
	assert ReviewedFile(MockBag([msg_error, msg_error, msg_error, msg_error, msg_error, msg_error])).rate == "C+"

	print "ALL TESTS OK"