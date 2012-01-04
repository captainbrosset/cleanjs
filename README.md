WHAT IS THIS?
============

cleanjs is a code review/check style kind of tool that can check javascript source files.
The tool is (for now) a command line python script.
The way it works is by parsing the source file then running a series checks on it, outputting info, warning and errors when needed.

The tool is focused on code quality. The following things (and others) are checked:
- file length
- function length
- variable and function name formatting and meaning
- comments
- complexity
- ...

USING CLEANJS
=============

cleanjs is written in python so, first, make sure you have python 2.7 installed and running.

Once you've retrieved the code, you can run the tool like this:

> python review.py path/to/my_source_file.js

This will review the file path/to/my_source_file.js and output the report in the console.

CONTRIBUTING
============

The easiest and most interesting way to contribute is to create more reviewers.

Check the /reviewers/ folder to see how they are made.

Each review must extend the BaseReviewer class and implement 1 method: review(self, file_data, message_bag)

- file_data is of type utils.filedata.FileData
- message_bag is of type utils.message.MessageBag

Check the TODO.txt file to see which reviewers are currently planned for development. Other general features of the tool are also described in this file.