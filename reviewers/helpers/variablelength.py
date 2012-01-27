import re

def get_variable_occurences_in_code(name, code):

	"""Return a tuple containing the line numbers of all occurences of variable name in code"""

	lines = code.split("\n")
	before_after_var = "[ \t\[\]\(\)\.\+\-\{\};:,]{1}"
	occurences = ()
	for index, line in enumerate(lines):
		occurs = not not re.findall(before_after_var + name + before_after_var, line)
		if occurs:
			occurences += index,
	return occurences

def get_variable_minmax_occurences_in_code(name, code):

	"""Return a tuple containing the min and max line numbers where variable name occurs in code"""

	occurences = get_variable_occurences_in_code(name, code)
	
	if len(occurences) > 0:
		return (min(occurences), max(occurences))
	else:
		return (0, 0)

def is_variable_name_too_short(name, code):

	"""Check whether a variable name is too short in the context of code
	This will check whether it is spread in the code rather than just relying on the variable name length)
	
	1 char variable length ==> maximum 3 consecutive lines
	2 chars variable length ==> maximum 4 consecutive lines
	3 chars variable length ==> maximum 5 lines between first and last occurences
	4 chars or more ==> ok
	"""

	is_toot_short = False

	minmax = get_variable_minmax_occurences_in_code(name, code)
	min_occurence = minmax[0]
	max_occurence = minmax[1]

	if len(name) == 1 and max_occurence - min_occurence > 2:
		is_toot_short = True
	if len(name) == 2 and max_occurence - min_occurence > 3:
		is_toot_short = True
	if len(name) == 3 and max_occurence - min_occurence > 5:
		is_toot_short = True

	return is_toot_short


if __name__ == "__main__":

	function_code = """
		var array = [1,2,3,4,5];
		var res = [];
		
		for(var i = 0; i < 12; i ++) {
			res.push(array[i]);
		}

		if(test) {
			res.push("test");
		}

		var re = /[a-z]*/gi;
		array.push("test".match(re))
		array.push("test2".match(re))

		re = null;

		delete array[0];

		return res;
	"""

	# Edge case:
	assert is_variable_name_too_short("doesnotexist", function_code) == False, "Variable does not even exist, should return False"
	# Normal cases:
	assert is_variable_name_too_short("i", function_code) == False, "Variable 'i' should not be considered too short because it's in a limited scope"
	assert is_variable_name_too_short("res", function_code) == True, "Variable 'res' should be considered too short because it's used across lot's of code"
	assert is_variable_name_too_short("re", function_code) == True, "Variable 're' should be considered too short because it's used across lot's of code"
	assert is_variable_name_too_short("array", function_code) == False, "Variable 'array' should not be considered too short because it's not ;-)"

	print "ALL TESTS OK"