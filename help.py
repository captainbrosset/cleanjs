from reviewers import codesize, comments, complexity, formatting, naming, unused, general

def output_reviewer_help(reviewer):
	help = "============================\n"
	help += reviewer.get_name() + ":\n"
	help += "---------------------------\n"
	help += reviewer.get_help()
	return help

print output_reviewer_help(general.Reviewer())	
print output_reviewer_help(codesize.Reviewer())
print output_reviewer_help(comments.Reviewer())
print output_reviewer_help(complexity.Reviewer())
print output_reviewer_help(formatting.Reviewer())
print output_reviewer_help(naming.Reviewer())
print output_reviewer_help(unused.Reviewer())
