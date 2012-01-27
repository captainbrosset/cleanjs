import re
import logging

from helpers import wordmeaning
from helpers import extractwords

logger = logging.getLogger(__name__)

class Reviewer():
	NB_OF_CHARS_IN_NAME_BEFORE_CAMELCASE = 15
	# Set to true to connect to the real dictionary
	DICT_WORD_CHECKING = False
	
	def get_name(self):
		return "naming"
		
	def get_help(self):
		return """Properly naming variables, arguments, functions or classes is key to making a code easy to read and maintain.
		This reviewer checks:
		- if a function returns something if its name starts with get, has or is
		- if a function accepts 1 argument if its name starts with set
		- if names are camelcased
		- if words in a camelcase name actually seem to mean something"""
	
	def name_starts_with(self, name, prefix):
		"""Returns true if name starts with prefix if prefix is "separated" from the rest of the string:
		- camelcase: "is" is the prefix of "isEmpty"
		- separator: "is" is the prefix of "is_empty"
		"""
		prefixlen = len(prefix)
		return name[0:prefixlen] == prefix and len(re.findall("[A-Z_]{1}", name[prefixlen:prefixlen+1])) == 1

	def review_gethasis_function_return(self, functions, message_bag):
		for function in functions:
			name = function.name
			is_gethasis = self.name_starts_with(name, "get") or self.name_starts_with(name, "is") or self.name_starts_with(name, "has")
			if is_gethasis and not function.has_return:
				message_bag.add_error(self, "Function " + name + " starts with 'is/has/get'. This usually means a return value is expected, but none was found.", function.line_nb);
	
	def review_set_function_arg(self, functions, message_bag):
		for function in functions:
			name = function.name
			is_set = self.name_starts_with(name, "set")
			if is_set and len(function.signature) == 0:
				message_bag.add_error(self, "Function " + name + " starts with 'set'. This usually means an argument is passed, but none was found.", function.line_nb);
	
	def review_all_names(self, vars, functions, message_bag):
		# Reviews function names, argument names and variable names only in fact
		# TODO: missing object properties checking too (this.xxx or prototype.something)
		all_objects = vars + functions

		for object in all_objects:
			words = extractwords.get_all_words_from_line(object.name)
			if getattr(object, "signature", None):
				for arg in object.signature:
					words += extractwords.get_all_words_from_line(arg)
			
			for word in words:
				word_exists = False
				if Reviewer.DICT_WORD_CHECKING:
					word_exists = wordmeaning.check_word_meaning_with_dict(word)
				else:
					word_exists = wordmeaning.check_word_meaning_with_letter_ratio(word)
				if not word_exists:
					message_bag.add_error(self, "Name " + word + " doesn't mean anything", object.line_nb)
	
	def review(self, file_data, message_bag):
		self.review_gethasis_function_return(file_data.functions, message_bag)
		self.review_set_function_arg(file_data.functions, message_bag)
		self.review_all_names(file_data.variables, file_data.functions, message_bag)


if __name__ == "__main__":
	class attrdict(dict):
		"""Used to easily mock modules dependencies"""
		def __init__(self, *args, **kwargs):
			dict.__init__(self, *args, **kwargs)
			self.__dict__ = self

	class MockMessageBag(object):
		def __init__(self):
			self.errors = []
		def add_error(self, reviewer, message, line=None):
			self.errors.append(message)
			
	reviewer = Reviewer()

	assert reviewer.name_starts_with("isEmpty", "is") == True
	assert reviewer.name_starts_with("something_nice", "something") == True
	assert reviewer.name_starts_with("hasTeeth", "has") == True
	assert reviewer.name_starts_with("is_green", "is") == True
	assert reviewer.name_starts_with("setup", "set") == False
	assert reviewer.name_starts_with("", "set") == False
	assert reviewer.name_starts_with("", "") == False

	def check_gethasis_functions_and_assert_bag_contains(functions, nb_expected_messages, msg):
		bag = MockMessageBag()
		reviewer.review_gethasis_function_return(functions, bag)
		assert len(bag.errors) == nb_expected_messages, msg

	def check_set_functions_and_assert_bag_contains(functions, nb_expected_messages, msg):
		bag = MockMessageBag()
		reviewer.review_set_function_arg(functions, bag)
		assert len(bag.errors) == nb_expected_messages, msg

	# Check that function starting with gethasis actually returns something
	function1 = attrdict(name="getSomeStuff", line_nb=0, has_return=True)
	function2 = attrdict(name="isEmpty", line_nb=0, has_return=True)
	function3 = attrdict(name="hasHairs", line_nb=0, has_return=True)
	check_gethasis_functions_and_assert_bag_contains([function1,function2,function3], 0, "Functions start with gethasis and returns something, should not output an error")

	# Check that functions starting with is has or get, but not followed by capital letter do not trigger any message
	function4 = attrdict(name="getho", line_nb=0, has_return=True)
	function5 = attrdict(name="israel", line_nb=0, has_return=False)
	function6 = attrdict(name="has", line_nb=0, has_return=False)
	function7 = attrdict(name="hasimut", line_nb=0, has_return=True)
	check_gethasis_functions_and_assert_bag_contains([function4,function5,function6,function7], 0, "All these functions start with get/has/is but not camelcased, so should not even look into them")
	
	# Check that function starting with set actually take arguments
	function10 = attrdict(name="setSomething", line_nb=0, signature=[])
	function11 = attrdict(name="setSomething", line_nb=0, signature=["something"])
	function12 = attrdict(name="setup", line_nb=0, signature=[])
	check_set_functions_and_assert_bag_contains([function10, function11, function12], 1, "Checking setter have parameter failed")

	print "ALL TESTS OK"