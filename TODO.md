Missing reviewers:
==================

- codesize
	- Length of this. variables
	- Line length: 80 warning, 120 error
- jsdoc
	- Private and protected have corresponding jsdoc, and opposite as well
	- Check jsdoc format and accepted @ statements
	- Check that jsdoc block have description
	- Check that file has first a license, then a jsdoc block that is at least some nb of lines with example. Display info if there is no `pre` tag cause it means there's no example
- unused
	- Unused fields this. In class
- code duplication
- jslint
	- new Array() and new Object()
	- check for global vars assignments (missing var)
	- check ; is present after assignements
- complexity
	- inline function is often sign of difficult to read code
	- try to check for long functions with several returns ...
- comments:
	- If // multiline comments are license header/help/ ... then skip
	- Try to detect if a // comment line and the following code line share patterns. If they do, it probably means that the comment is useless
- vertical:
	- Review vertical distance inside prototype : properties should come first, functions then
	- Try to check flow of functions: caller before callee, vertically
- formatting:
	- Formatting: hard to rely on function declaration because formatters might be differently configured. However should check for = assignment (a = 1).
	- Should also try to see if tab an spaces are mixed
	- Check if multiple spaces or tabs are used after some content(could be to space things and align vertically multiple lines) this is bad, should only be one whitespace between words and statements
	- Could check if there are not any empty line in a long function, it means that blocks are not separated nicely

Other misc stuff to do:
=======================

- Redo the layout of the HTML code output (separate code and messages in 2 columns like http://rtomayko.github.com/rocco/)
- Make reviewer expose configs so this can be configured before running
- Class parsing (Parse prototype and all its functions and properties)
- Automatically run in eclipse while saving a js class file
- Website to run this on a textarea containing js code
- Give listof msgs at the end + a grade with funny random sentence. Offer animated gif if class passed all reviewers.
- Run stats on the overall code quality of all submitted code.
- Extract messages as constants of each reviewer class with %n replacement chars (easier for unit testing then)
- Try to use jslint (in python) as a parser ? Could help for parsing, although the simple parser in place today is probably enough
- Continue writing unit tests for all other reviewers (think of a better way to mock (for now, the whole parsing is done))
- Change look and feel of the html output: bigger, with border and or shadow for messages
- Fix problem with the last line in function appearing into the total_lines array of line_data
- Local dictionary for names reviewer: fill it in by running a script at night that will connect to wordreference every X seconds