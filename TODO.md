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
- duplication
	
Other misc stuff to do:
=======================

- Fix nested functions problem
- Automatically run in eclipse while saving a js class file
- Categorize reviewers by file types (tpls, css, js...)
- Website to run this on a textarea containing js code
- Give listof msgs at the end + a grade with funny random sentence. Offer animated gif if class passed all reviewers.
- Run stats on the overall code quality of all submitted code.
- Make reviewer expose configs so this can be configured before running
- Add appender/filter like functionality on the report (via command line arguments)
- Sort messages per category
- pre-pad report with spaces so that all report lines are aligned
- Make it possible for users to define more custom reviewer, by configuration (from a different directory)
- Make it possible for users to define more custom parsers, by configuration (from a different directory)
- The table-like console output for messages is fun, but not very useful, and code isn't clean. Extract this into an appender
	- possibility to add other appenders (for the website for instance)
- Extract messages as constants of each reviewer class with %n replacement chars (easier for unit testing then)
- Unit test each reviewer
- Class parsing