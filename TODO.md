Missing reviewers:
==================

- codesize
	- Length of this. variables
- jsdoc
	- Private and protected have corresponding jsdoc, and opposite as well
	- Check jsdoc format and accepted @ statements
	- Check that jsdoc block have description
	- Check that file has first a license, then a jsdoc block that is at least some nb of lines with example. Display info if there is no `pre` tag cause it means there's no example
- unused
	- Unused fields this. In class
- code duplication
	- comparing branches of the AST ?
- syntax
	- jslint
	- new Array() and new Object()
	- check for global vars assignments (missing var)
	- check ; is present after assignements
	- Check that when a local method is called, it is called with the right number of arguments
- complexity
	- inline function is often sign of difficult to read code
- comments:
	- If // multiline comments are license header/help/ ... then skip
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
	- When checking the meaning of one letter words like i (for indexes), we report an error, even if the codesize module accepted it because it was in a limited scope ... How do we deal with this? Should naming have a dependency on codesize?
	
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
- Find a way to have errors/warnings/infos into the editor directly, rather than in the console