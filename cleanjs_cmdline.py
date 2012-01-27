"""
This is the command line tool for cleanjs.
Usage example:
python cmdline.py /my/source/file.js /path/to/myReport.html

Note that it's simple to integrate cleanjs in any other type of
python 2.7 enabled system. See the source code below to understand
how easy it is to review a file using the fileparser, reviewer and
reporter
"""

# This tool works on the command line, so needs to use commant line arguments
import sys

if len(sys.argv) != 3:
	print ""
	print "This command line tool requires 2 arguments:"
	print "  - the javascript file path to be checked"
	print "  - the path and filename of the report HTML file that will be created"
	print ""
	print "Usage example: $ python cleanjs_cmdline.py path/to/myFile.js path/to/myFileReport.html"
	print ""
	exit()

file_name = sys.argv[1]
report_name = sys.argv[2]

# Gather data about the file to be reviewed
from parsers import fileparser
file_data = fileparser.get_file_data_from_file(file_name)

# Review the file
from reviewers import reviewer
result = reviewer.review(file_data)

# Displaying the messages to an output
from reporters import htmlwithcode
htmlwithcode.output_messages(result, file_data, report_name)

print "Your file has been cleanjs'd! Check the report here " + report_name