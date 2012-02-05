from collections import *

from pynarcissus import jsparser

class ParsingError(Exception):
	def __init__(self, error):
		message = "Syntax error line " + str(self.get_line_number(error)) + " : " + self.get_msg(error)
		Exception.__init__(self, message)

	def get_msg(self, error):
		return str(error).split("\n")[0]
	
	def get_line_number(self, error):
		return int(str(error).split("\n")[1].split(":")[1])

class JSFileParser:
	"""The js file parser can parse js source code and iterate over its AST.
	It can accept any number of visitors (via add_visitor).
	
	Example:

	parser = JSFileParser(content)
	parser.add_visitor(MyVisitor())
	parser.parse()"""
	
	CHILD_ATTRS = ['value', 'thenPart', 'elsePart', 'expression', 'body','exception', 'initializer',
	'tryBlock', 'condition','update', 'iterator', 'object', 'setup', 'discriminant', 'finallyBlock',
	'tryBlock', 'varDecl', 'target']

	def __init__(self, source):
		self.visited = list()
		self.source = source
		self.visitors = []
		try:
			self.root = jsparser.parse(self.source)
		except jsparser.ParseError as error:
			raise ParsingError(error)
	
	def review(self, file_data, message_bag):
		try:
			ast = jsparser.parse(file_data.content)
		except jsparser.ParseError as error:
			message_bag.add_error(self, self.extract_error_msg(error), self.extract_error_line(error))

	def get_visitors(self):
		return self.visitors

	def look4Childen(self, node):
		for attr in self.CHILD_ATTRS:
			child = getattr(node, attr, None)
			if isinstance(child, jsparser.Node):
				self.visit(child)

	def add_visitor(self, visitor):
		self.visitors.append(visitor)

	def exec_visitors_on_node(self, node, source):
		self.exec_visitors_function("visit_%s" % node.type, source, node)
			
	def exec_preprocess_visitors(self, source):
		self.exec_visitors_function("visit_PREPROCESS", source)
	
	def exec_postprocess_visitors(self, source):
		self.exec_visitors_function("visit_POSTPROCESS", source)
	
	def exec_visitors_function(self, function_name, source, node=None):
		for visitor in self.visitors:
			visitor_func = getattr(visitor, function_name, None)
			visitor_anynode_func = getattr(visitor, "visit_ANY", None)
			if visitor_func and node:
				visitor_func(node, source)
			elif visitor_anynode_func and node:
				visitor_anynode_func(node, source)
			elif visitor_func and not node:
				visitor_func(source)

	def parse(self):
		self.exec_preprocess_visitors(self.source)
		self.visit()
		self.exec_postprocess_visitors(self.source)

	def visit(self, root=None):
		if not root:
			root = self.root
		
		if id(root) in self.visited:
			return
		
		self.visited.append(id(root))
		
		self.exec_visitors_on_node(root, self.source)
			
		self.look4Childen(root)
		for node in root:
			self.visit(node)
		

if __name__ == "__main__":
	content = """
	//TODO: do something here
	// There are plenty of things to explain about this file, because it is very very complex

	function hasWings() {
		doSomething()
		doSomethingElse()
		butNeverReturn();
	}

	function setSomething() {
		// this method does something
		var a = 1;
		// For loop
		for(var i = 0; i < 4; i ++) {
			// comment 1
			// comment 2
			var thisisaverylsdfhsdfsdgasdghongvdfhdfhariablename; // this variable does something
		} // end for
		// End of for loop
	}

	// --------------- another part of my file ---------------

	function t() {}

	function averyloingnameforafunctionisnotverygood(foo, bar) {}

	function test(a,b,c,b,d,d,d) {
		var test;		
		if(test && test || test) {
			
		}
		// FIXME: not working
	}

	var MyClass = function(a,b){
		// test
		this.a = a;
		this.b = b;
		var that = this;
		this.constructorInnerFunction = function(thing) {
			return that.a + that.b + thing;
		}
	};
	MyClass.prototype = {
		getSomething: function() {
			this.callback(function(closureArg) {
				return closureArg + 2;
			});
			return 0;
		}
	};

	function ctrlMgr() {
		if(true) {
			if(true) {
				while(true) {
					if(something || somethingelse && (anotherthing || !what)) {
						if(test) {
							var a = {
								doSomething: function(arg) {
									// test
								}
							};
							return a;
						} else {
							return 1;
						}
					} // end if
				} // end while
			}
		}
	}"""
	parser = JSFileParser(content)
	
	from functionparser import FunctionParser
	function_visitor = FunctionParser()
	parser.add_visitor(function_visitor)
			
	parser.parse()
		
	assert len(function_visitor.functions) == 10, "Wrong number of functions in the file"
	function_names = []
	for f in function_visitor.functions:
		function_names.append(f.name)
	assert "".join(sorted(function_names)) == "MyClassaveryloingnameforafunctionisnotverygoodconstructorInnerFunctionctrlMgrdoSomethinggetSomethinghasWingssetSomethingttest", "Wrong functions found in the file"
	
	function_return_code = """
	function test() {
		return doSomething();
	}

	var anotherTest = function() {
		return object.doSomething();
	}
	"""
	parser = JSFileParser(function_return_code)
	parser.parse()

	print "ALL TESTS OK"