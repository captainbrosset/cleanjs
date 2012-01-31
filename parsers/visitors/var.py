import visitor

class Var(visitor.Entity):
	"""Represents a variable assignment in the parsed source file"""
	
	def __init__(self, name, line_number, start_pos, end_pos):
		super(Var, self).__init__(line_number, start_pos, end_pos)
		
		self.name = name
		
	def __repr__(self):
		return "var " + self.name + " (line " + str(self.line_number) + ")"

class VarVisitor:
	"""Var visitor implementation.
	
	Reacts to certain nodes in the tree in order to gather all variable
	assignments inside the parsed JS file
	
	When visit is done, this visitor holds an array of Var objects in
	visitor.result"""

	def __init__(self):
		self.entities = []
		
	def __repr__(self):
		result = ""
		for this in self.entities:
			result += "- " + str(this) + "\n"
		return result

	def add_var(self, name, line_number, start, end):
		is_already_there = False
		for var in self.entities:
			if var.name == name and var.line_number == line_number:
				is_already_there = True
		
		if not is_already_there:
			self.entities.append(Var(name, line_number, start, end))

	def visit_VAR(self, node, source):
		if getattr(node[0], "initializer", False):
			self.add_var(node[0].value, node.lineno, node.start, node[0].initializer.end)
		else:
			self.add_var(node[0].value, node.lineno, node.start, node.end)