import visitor

class Function(visitor.Entity):
	"""Represents a function in the parsed source file"""
	
	def __init__(self, name, body, line_number, arguments, start_pos, end_pos):
		super(Function, self).__init__(line_number, start_pos, end_pos)
		
		self.name = name
		self.body = body
		self.arguments = arguments
		
	def __repr__(self):
		return "Function " + self.name + "(" + str(self.arguments) + ") (line " + str(self.line_number) + ")"

class FunctionVisitor:
	"""Function visitor implementation.
	
	Reacts to certain nodes in the tree in order to gather all functions
	inside the parsed JS file (named functions, anonymous functions)
	
	When visit is done, this visitor holds an array of Function objects in
	visitor.result"""

	def __init__(self):
		self.entities = []
		
	def __repr__(self):
		result = ""
		for function in self.entities:
			result += "- " + str(function) + "\n"
		return result
		
	def visit_FUNCTION(self, node, source):
		# Named functions only, the getattr returns None if name doesn't exist
		if node.type == "FUNCTION" and getattr(node, "name", None):
			self.entities.append(Function(node.name, source[node.start:node.end], node.lineno, node.params, node.start, node.end))

	def visit_IDENTIFIER(self, node, source):
		# Anonymous functions declared with var name = function() {};
		try:
			if node.type == "IDENTIFIER" and hasattr(node, "initializer") and node.initializer.type == "FUNCTION":
				self.entities.append(Function(node.name, source[node.start:node.initializer.end], node.lineno, node.initializer.params, node.start, node.initializer.end))
		except Exception as e:
			pass

	def visit_ASSIGN(self, node, source):
		if node[1].type == "FUNCTION":
			self.entities.append(Function(node[0].value, source[node[1].start:node[1].end], node[1].lineno, node[1].params, node[1].start, node[1].end))

	def visit_PROPERTY_INIT(self, node, source):
		# Anonymous functions declared as a property of an object
		try:
			if node.type == "PROPERTY_INIT" and node[1].type == "FUNCTION":
				self.entities.append(Function(node[0].value, source[node.start:node[1].end], node[0].lineno, node[1].params, node.start, node[1].end))
		except Exception as e:
			pass