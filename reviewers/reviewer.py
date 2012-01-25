import syntax, codesize, comments, complexity, formatting, naming, unused, general
from messagebag import MessageBag

def review(file_data):
	message_bag = MessageBag()

	syntax.Reviewer().review(file_data, message_bag)
	general.Reviewer().review(file_data, message_bag)
	codesize.Reviewer().review(file_data, message_bag)
	comments.Reviewer().review(file_data, message_bag)
	complexity.Reviewer().review(file_data, message_bag)
	formatting.Reviewer().review(file_data, message_bag)
	naming.Reviewer().review(file_data, message_bag)
	unused.Reviewer().review(file_data, message_bag)

	result = {
		"message_bag": message_bag,
		"rating": get_rate(file_data, message_bag)
	}

	return result

def get_rate(file_data, message_bag):
	nb_warnings = 0
	nb_errors = 0

	for msg in message_bag.get_messages():
		if msg.type == "warning":
			nb_warnings += 1
		if msg.type == "error":
			nb_errors += 1

	# errors are 3 times more important than warnings
	total_nb_of_msgs = int(round(float(nb_errors * 3 + nb_warnings) / 3))
	if total_nb_of_msgs > 18:
		total_nb_of_msgs = 18

	rating = ["A+","A","A-","B+","B","B-","C+","C","C-","D+","D","D-","E+","E","E-","F+","F","F-"][total_nb_of_msgs]

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
	
	assert get_rate(None, MockBag([msg_warning,msg_warning,msg_warning,msg_warning,msg_warning])) == "C"
	assert get_rate(None, MockBag([msg_error,msg_error,msg_error,msg_error])) == "E"
	assert get_rate(None, MockBag([])) == "A"
	assert get_rate(None, MockBag([msg_error, msg_error, msg_warning])) == "C"
	assert get_rate(None, MockBag([msg_error, msg_error, msg_error, msg_error, msg_error, msg_error])) == "really really bad"

	print "ALL TESTS OK" + __file__