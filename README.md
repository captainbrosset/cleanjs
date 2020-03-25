**UNMAINTAINED REPOSITORY** (issues are closed, no more development)

WHAT IS THIS?
============

cleanjs is a tool written in python that checks javascript source files and returns a report about various aspects related to **clean code** practices (kind of like check style).

The way it works is by parsing the source file then running a series checks on it, outputting info, warning and errors when needed.

The tool is focused on code quality. The following things (and others) are checked:

- file length
- function length
- variable and function name formatting and meaning
- comments
- complexity
- syntax error
- formatting
- ...

USING CLEANJS
=============

The first way to use cleanjs is online: http://cleanjscode.appspot.com/

If you are interested in running it locally on your computer and integrate it into some build system, then read on:

cleanjs is written in python so, first, make sure you have [python 2.7 installed and running](http://python.org/getit/) (seems to work with 2.6 but mostly untested).

Get cleanjs by downloading [one of the tags](https://github.com/captainbrosset/cleanjs/tags).

Once you've retrieved the code, you can run the tool like this:

    python cleanjs_cmdline.py path/to/my_source_file.js path/to/output/file.html

This will review the file path/to/my_source_file.js and create an HTML report file.

You can check the testscript/reports/*.html files to see examples of reports

Optionally, if you are using a text editor like [Sublime Text](http://sublimetext.com) or any other editor able to run build commands on files, you can use the `cleanjs_sublime.py` entry point instead.

USING IN SUBLIME TEXT 2
=======================

cleanjs can also be integrated into Sublime Text 2 as a plugin.

If you have [Sublime Text 2](http://www.sublimetext.com/2) with [Package Control](http://wbond.net/sublime_packages/package_control), just launch package control, select "Add Repository", enter https://github.com/captainbrosset/cleanjs and then launch "install package" and select cleanjs from the list.

The default key biding is `ctrl+shift+c` and for now only outputs messages to a panel and highlights the corresponding lines in the text.

A tooltip/line gutter API is terribly missing in Sublime Text 2 at the moment, [vote for it here](http://sublimetext.userecho.com/topic/54838-/).

GOING FURTHER
=============

Integrating cleanjs into an existing python program is fairly easy. Open `cleanjs_cmdline.py` to see how a file is parsed, how reviewers are called and how the output is constructed. You'll see it's easy to create your own reviewers and reporters.

CONTRIBUTING
============

The easiest and most interesting way to contribute is to create more reviewers.

Check the `/reviewers/` folder to see how they are made.

Each reviewer must define a `Reviewer` class and implement a method: `review(self, file_data, message_bag)`

- file_data is of type `parsers.fileparser.FileData`
- message_bag is of type `reviewers.messagebag.MessageBag`

Check the issues in GitHub to see what is currently planned for development.
