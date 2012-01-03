import sys
import os
import re

from utils import reviewerloader, message, parser, filedata

# Dealing with the file itself, getting its content
src_file_name = sys.argv[1]
src_file = open(src_file_name, 'r')
src_file_content = src_file.read()
src_file_lines = re.findall("^(.*)$", src_file_content, flags=re.MULTILINE);

# Getting some structured data from the file
parser = parser.Parser()
src_file_functions = parser.parse_functions(src_file_content)
src_file_variables = parser.parse_variables(src_file_content)

# Preparing the file wrapper
file_data = filedata.FileData(src_file_name, src_file_content, src_file_lines, src_file_functions, src_file_variables)

# Preparing the message bag
review_message_bag = message.MessageBag()

# Loading and executing all reviewers
reviewer_modules_to_import = []
for reviewer_file_name in os.listdir("reviewers"):
    if reviewer_file_name != "__init__.py" and reviewer_file_name[-3:] != "pyc" and reviewer_file_name != "base.py" and reviewer_file_name != "base.pyc":
        reviewer = reviewerloader.load_from_file("reviewers/" + reviewer_file_name, "Reviewer")
        reviewer.review(file_data, review_message_bag)

print review_message_bag.report_messages(src_file_name)