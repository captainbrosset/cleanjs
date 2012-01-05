Missing reviewers:
==================

- codesize
	- Length of this. variables
- clean names
	- Check words (in camelcase expression) against a mini dictionary?
	- Refuse known patterns like mgr, sz, len, idx, ...
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
- complexity
	- inline function is often sign of difficult to read code
	- try to check for long functions with several returns ...
- comments:
	- If // multiline comments are license header/help/ ... then skip
	
Other misc stuff to do:
=======================

- Transform the reviewer utils module into a code extraction helper, and add methods to get nb of lines of comments, nb of lines of code, nb of total lines in a file, or a piece of string, or function. Or put this at parsing level once and for all. And in fact, in the file data object passed to reviewer, should have sub-objects and/or methods to get line numbers for match patterns, etc ... so that reviewers do as little as possible
- change reviewers to only be simple py modules with functions (don't think classes are needed, and they make the use of reviewers harder). 
- Fix nested functions problem
- Automatically run in eclipse while saving a js class file
- Categorize reviewers by file types (tpls, css, js...)
- Website to run this on a textarea containing js code
- Give listof msgs at the end + a grade with funny random sentence. Offer animated gif if class passed all reviewers.
- Run stats on the overall code quality of all submitted code.
- Make reviewer expose configs so this can be configured before running
- Sort messages per category
- Extract messages as constants of each reviewer class with %n replacement chars (easier for unit testing then)
- Unit test each reviewer. Put the test code inside each reviewer. Will need a mini-framework to easily test a reviewer
- Class parsing
- Try to use jslint (in python) as a parser
