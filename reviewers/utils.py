def get_line_nb_for_match_in_str(content, match):
	return content[0:match.start()].count("\n") + 1