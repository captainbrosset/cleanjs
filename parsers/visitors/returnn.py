import visitor

class Return(visitor.Entity):
	"""Represents a return statement in the parsed source file"""
	
	def __init__(self, line_number, start_pos, end_pos):
		super(Return, self).__init__(line_number, start_pos, end_pos)
		
	def __repr__(self):
		return "return (line " + str(self.line_number) + ")"

class ReturnVisitor:
	"""Return visitor implementation.
	
	Reacts to certain nodes in the tree in order to gather all return
	statements inside the parsed JS file
	
	When visit is done, this visitor holds an array of Return objects in
	visitor.result"""

	def __init__(self):
		self.entities = []
		
	def __repr__(self):
		result = ""
		for this in self.entities:
			result += "- " + str(this) + "\n"
		return result

	def visit_RETURN(self, node, source):
		self.entities.append(Return(node.lineno, node.start, node.end))