Missing reviewers:
==================

- codesize
	- Length of this. variables
	- Line length: 80 warning, 120 error
	- length of variable checker is fine, except when it checks for one or two letter words that are in fact in the dictionary ... 
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
- naming:
	- review name meaning for object properties too (like this.xxx or prototype.xxx or myobj.xxx)
	
Other misc stuff to do:
=======================

- Make reviewer expose configs so this can be configured before running
- Class parsing (Parse prototype and all its functions and properties)
- Automatically run in eclipse while saving a js class file
- Extract messages as constants of each reviewer class with %n replacement chars (easier for unit testing then)
- Continue writing unit tests for all other reviewers (think of a better way to mock (for now, the whole parsing is done))
- Local dictionary for names reviewer: fill it in by running a script at night that will connect to wordreference every X seconds
- Parser:
	- https://gist.github.com/1607354 is a good example
	- http://ominian.com/2012/01/06/working-with-using-pynarcissus-to-parse-javascript-in-python/
	- parser originally is pynarcissus
