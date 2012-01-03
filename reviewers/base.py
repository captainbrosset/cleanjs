class BaseReviewer:
	def set_name(self, name):
		self.name = name
	def get_name(self):
		return self.name	
	def get_line_nb_for_match_in_str(self, content, match):
		return content[0:match.start()].count("\n") + 1