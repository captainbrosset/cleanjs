class Entity(object):
	"""Base class for JS objects"""
	
	def __init__(self, line_number, start_pos, end_pos):
		self.line_number = line_number
		self.start_pos = start_pos
		self.end_pos = end_pos
	
	def __repr__(self):
		return "Entity line " + str(self.line_number)
	
class Visitor:
	"""Abstract Visitor class.
	
	Visitors can implement any number of visit_<NODETYPE> methods.
	If a visitor implements visit_FUNCTION for instance, this method
	will be called anytime TreeVisitorHandler loops over a FUNCTION
	node. The 2 arguments being passed to the visitor are:
	- the node
	- the complete source code of the file
	
	Visitors may also implement a visit_FILECONTENT method.
	This method will NOT be called when nodes are traversed in the tree
	but only once at the beginning of the visiting. The argument passed is:
	- the complete source code of the file
	
	The job of a visitor is to create Entity objects in self.entities."""
	
	def visit_ANY(self):
		pass