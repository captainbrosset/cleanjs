def filter_empty_items_from_dict_list(list, object_property_to_check):
	"""Given a list of dictionaries, filter out the ones for which the
	object_property_to_check key/value evaluates to False"""

	return filter(lambda item: not not item[object_property_to_check], list)

def filter_dups_from_list(the_list):
	"""Given a list of hashable items, remove the duplicates from that list"""

	return list(set(the_list))

if __name__ == "__main__":
	assert filter_empty_items_from_dict_list([], "test") == []
	assert filter_empty_items_from_dict_list([{"test": ""}, {"test": []}, {"test": "a"}], "test") == [{"test": "a"}]

	assert filter_dups_from_list([]) == []
	assert filter_dups_from_list([1,1,1,2,3,1,5]) == [1,2,3,5]
	assert sorted(filter_dups_from_list(["a", 4, False, False, 4, "a", "b"])) == sorted(["a", 4, False, "b"])

	print "ALL TESTS OK"