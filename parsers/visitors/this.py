import visitor

class This(visitor.Entity):
	"""Represents a property assignment to this in the parsed source file"""
	
	def __init__(self, name, line_number, start_pos, end_pos):
		super(This, self).__init__(line_number, start_pos, end_pos)
		
		self.name = name
		
	def __repr__(self):
		return "this." + self.name + " (line " + str(self.line_number) + ")"

class ThisVisitor:
	"""This visitor implementation.
	
	Reacts to certain nodes in the tree in order to gather all assignments
	to <this> inside the parsed JS file
	
	When visit is done, this visitor holds an array of This objects in
	visitor.result"""

	def __init__(self):
		self.entities = []
		
	def __repr__(self):
		result = ""
		for this in self.entities:
			result += "- " + str(this) + "\n"
		return result

	def add_this(self, name, line_number, start, end):
		is_already_there = False
		for this in self.entities:
			if this.name == name and this.line_number == line_number:
				is_already_there = True
		
		if not is_already_there:
			self.entities.append(This(name, line_number, start, end))

	def visit_DOT(self, node, source):
		if node[0].type == "THIS":
			self.add_this(node.value, node.lineno, node.start, node.end)