Missing reviewers:
==================

- codesize
	- Length of this. variables
- clean names
	- Check words (in camelcase expression) against a mini dictionary (could be dynamic, if a word doesn't exist, look for it using a web service like word reference and then add it to the local dictionnary if it exists)
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

- Fix nested functions problem
- Make reviewer expose configs so this can be configured before running
- Class parsing
- Automatically run in eclipse while saving a js class file
- Website to run this on a textarea containing js code
- Give listof msgs at the end + a grade with funny random sentence. Offer animated gif if class passed all reviewers.
- Run stats on the overall code quality of all submitted code.
- Extract messages as constants of each reviewer class with %n replacement chars (easier for unit testing then)
- Try to use jslint (in python) as a parser ? Could help for parsing, although the simple parser in place today is probably enough