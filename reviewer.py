from reviewers import codesize, comments, complexity, formatting, naming, unused, general
from messagebag import MessageBag

def review(file_data):
	message_bag = MessageBag()

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
	global_rate = int(float(nb_errors * 3 + nb_warnings) / 4)
	if global_rate > 26:
		global_rate = 26

	rating = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"][int(global_rate) - 1]

	return rating