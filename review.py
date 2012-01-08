# logging
import logging
logging.basicConfig(format="%(asctime)s | %(levelname)s | %(module)s | %(message)s", level=logging.DEBUG)

# Gather data about the file to be reviewed
import sys
import fileparser
file_data = fileparser.get_file_data_from_file(sys.argv[1])

# Prepare a message bag to put infos, warnings and errors
from messagebag import MessageBag
message_bag = MessageBag()

# Execute all needed reviewers, passing the message bag
from reviewers import codesize, comments, complexity, formatting, naming, unused, general
general.Reviewer().review(file_data, message_bag)
codesize.Reviewer().review(file_data, message_bag)
comments.Reviewer().review(file_data, message_bag)
complexity.Reviewer().review(file_data, message_bag)
formatting.Reviewer().review(file_data, message_bag)
naming.Reviewer().review(file_data, message_bag)
unused.Reviewer().review(file_data, message_bag)
    
# Displaying the messages to an output
from reporters import htmlwithcode
htmlwithcode.output_messages(message_bag, file_data)