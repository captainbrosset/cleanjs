USING CLEANJS
=============

$ python review.py my_source_file.js

This will review the file my_source_file.js and output a list of warnings and errors to the console.

Messages are output by reviewers.
There are reviewers for file size, complexity, naming, etc ...

CONTRIBUTING
============

The easiest and most interesting way to contribute is to create more reviewers.

Check the /reviewers/ folder to see how they are made.

Each review must extend the BaseReviewer class and implement 1 method: review(self, file_data, message_bag)

file_data is of type utils.filedata.FileData

message_bag is of type utils.message.MessageBag

Check the TODO.txt file to see which reviewers are missing