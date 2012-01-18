"""
This is the sublime text integration of cleanjs.
"""

import sys
import fileparser
file_data = fileparser.get_file_data_from_file(sys.argv[1])

import reviewer
result = reviewer.review(file_data)

for msg in result["message_bag"].get_messages():
	line = None
	if msg.line:
		line = str(msg.line)
	else:
		line = "1"
	print sys.argv[1] + "|" + line + "|0|" + msg.reviewer + " " + msg.type + " > " + msg.content