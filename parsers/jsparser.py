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

class JSFileParser(object):
	def __init__(self):
		self.parsing_error = None
	
	def is_parsed(self):
		return self.parsing_error == None

	def parse(self, source):
		ast = None
		try:
			ast = jsparser.parse(source)
		except jsparser.ParseError as error:
			self.parsing_error = ParsingError(error)
		return ast

class JSFileVisitorHandler(object):
	"""The js file visitor can visit a parsed js source code and iterate over its AST.
	It can accept any number of visitors (via add_visitor).
	
	Example:

	visitor_handler = JSFileVisitorHandler(content)
	visitor_handler.add_visitor(MyVisitor())
	visitor_handler.visit()"""
	
	CHILD_ATTRS = ['value', 'thenPart', 'elsePart', 'expression', 'body', 'exception', 'initializer',
    'tryBlock', 'condition', 'update', 'iterator', 'object', 'setup', 'discriminant', 'finallyBlock',
    'catchClauses', 'varDecl', 'target', 'cases', 'caseLabel', 'statements', 'varDecls', 'funDecls']

	def __init__(self, source):
		self.visited = list()
		self.source = source
		self.visitors = []

		self.parser = JSFileParser()
		self.root = self.parser.parse(self.source)
	
	def get_visitors(self):
		return self.visitors

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

	def visit(self):
		if self.parser.is_parsed():
			self.exec_preprocess_visitors(self.source)
			self._walk_node()
			self.exec_postprocess_visitors(self.source)
		else:
			raise self.parser.parsing_error
	
	def _walk_node(self, root=None):
		if not root:
			root = self.root
		
		if id(root) in self.visited:
			return
		self.visited.append(id(root))

		self.exec_visitors_on_node(root, self.source)

		for attr in self.CHILD_ATTRS:
			child = getattr(root, attr, None)
			if isinstance(child, jsparser.Node):
				self._walk_node(child)
			if isinstance(child, list):
				for c in child:
					if isinstance(c, jsparser.Node):
						self._walk_node(c)

		for node in root:
			self._walk_node(node)
		

if __name__ == "__main__":
	from functionparser import FunctionParser

	inner_function = """
	function ctrlMgr() {
		if(true) {
			if(true) {
				while(true) {
					if(something || somethingelse && (anotherthing || !what)) {
						if(test) {
							var a = {
								doSomething: function() {
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
	}
	"""
	handler = JSFileVisitorHandler(inner_function)
	function_visitor = FunctionParser()
	handler.add_visitor(function_visitor)	
	handler.visit()
	assert function_visitor.functions[0].variables[0].name == "a"

	complex_code = """
	function name() {
		if(test && test2 || true) {
			while(true) {
				for(var i = 0; i < 4; i ++) {
					try {
						switch (test) {
							case 1:
								alert("")
							break;
							default:
								alert("");
							break;
						}
					} catch (e) {
						alert("")
					}
				}
			}
		}
		return 3;
	}
	"""
	handler = JSFileVisitorHandler(complex_code)
	function_visitor = FunctionParser()
	handler.add_visitor(function_visitor)	
	handler.visit()
	assert function_visitor.functions[0].complexity == 10
	assert function_visitor.functions[0].nb_return == 1

	return_code = """
	Apple.prototype.getInfo = function() {
    return this.color + ' ' + this.type + ' apple';
	};
	"""
	handler = JSFileVisitorHandler(return_code)
	function_visitor = FunctionParser()
	handler.add_visitor(function_visitor)	
	handler.visit()
	assert function_visitor.functions[0].complexity == 1
	assert function_visitor.functions[0].nb_return == 1

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
	parser = JSFileVisitorHandler(content)
	
	function_visitor = FunctionParser()
	parser.add_visitor(function_visitor)
			
	parser.visit()
		
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
	parser = JSFileVisitorHandler(function_return_code)
	assert parser.parser.parsing_error == None
	parser.visit()

	var_usage = """var a = multiply/2;
	var b = a*multiply+(multiply/multiply)
	"""
	JSFileVisitorHandler(var_usage)

	handler = JSFileVisitorHandler("return object.doSomething();")
	assert handler.parser.parsing_error != None

	print "ALL TESTS OK"