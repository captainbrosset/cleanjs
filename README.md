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

Get cleanjs by downloading one of the tags available on the project Tags page.

Once you've retrieved the code, you can run the tool like this:

    python review.py path/to/my_source_file.js path/to/output/folder

This will review the file path/to/my_source_file.js and create an HTML report file.

You can check the testscript/reports/*.html files to see examples of reports

GOING FURTHER
=============

Integrating cleanjs into an existing python program is fairly easy. Open review.py to see how a file is parsed, how reviewers are called and how the output is constructed. You'll see it's easy to create your own reviewers and reporters.

CONTRIBUTING
============

The easiest and most interesting way to contribute is to create more reviewers.

Check the /reviewers/ folder to see how they are made.

Each review must extend the BaseReviewer class and implement 1 method: review(self, file_data, message_bag)

- file_data is of type fileparser.FileData
- message_bag is of type messagebag.MessageBag

Check the TODO.md file to see which reviewers are currently planned for development. Other general features of the tool are also described in this file.