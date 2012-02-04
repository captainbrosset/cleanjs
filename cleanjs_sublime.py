class attrdict(dict):
	"""Used to easily mock modules dependencies"""
	def __init__(self, *args, **kwargs):
		dict.__init__(self, *args, **kwargs)
		self.__dict__ = self

import sys

try:
	import sublime, sublime_plugin
except:
	# Mocking out dependencies in case of unit testing
	# FIXME: How to make this more elegant ???
	sublime = {}
	class TextCommand:
		pass
	class EventListener:
		pass
	sublime_plugin = attrdict(TextCommand=TextCommand, EventListener=EventListener)

from parsers import fileparser
from reviewers import reviewer

REGIONS_KEY = PANEL_KEY = "CLEANJS"

class CleanjsCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		#settings = self.view.settings()
		js_code = self.view.substr(sublime.Region(0, self.view.size()))

		file_data = None
		try:
			file_data = fileparser.get_file_data_from_content("sublime cleanjs", js_code)
		except Exception as error:
			self.show_messages_to_panel(str(error), PANEL_KEY)
			return

		result = reviewer.review(file_data)

		text = self.get_full_report_from_result(result)

		self.show_messages_to_panel(text, PANEL_KEY)
		self.show_messages_to_regions(result.message_bag.get_messages(), file_data.lines)
	
	def get_full_report_from_result(self, result):
		text = "Rate : " + result.rate + "\n"
		messages = result.message_bag.get_messages()
		for message in messages:
			if message.reviewer != "general":
				text += "\nline " + str(message.line) + " | " + message.reviewer + " " + message.type + " : " + message.content
		return text

	def show_messages_to_regions(self, messages, file_lines):
		self.view.erase_regions(REGIONS_KEY)

		regions = []
		for message in messages:
			if message.line:
				points = self.get_points_from_line(message.line, file_lines)
				regions.append(sublime.Region(points[0], points[1]))

		self.view.add_regions(REGIONS_KEY, regions, "string", sublime.DRAW_OUTLINED)

	def get_points_from_line(self, line_number, file_lines):
		start = 0
		end = 0
		for index, line in enumerate(file_lines.all_lines):
			if index+1 == line_number:
				end = start + len(line.complete_line)
				break
			start += len(line.complete_line) + 1
		return (start, end)

	def show_messages_to_panel(self, text, panel_name = 'example'):
		# get_output_panel doesn't "get" the panel, it *creates* it, 
		# so we should only call get_output_panel once
		if not hasattr(self, 'output_view'):
			self.output_view = self.view.window().get_output_panel(panel_name)
		v = self.output_view

		# Write this text to the output panel and display it
		edit = v.begin_edit()
		v.erase(edit, sublime.Region(0, v.size()))
		v.insert(edit, v.size(), text)
		v.end_edit(edit)
		v.show(v.size())

		self.view.window().run_command("show_panel", {"panel": "output." + panel_name})

class EventListener(sublime_plugin.EventListener):
	def on_modified(self, view):
		view.erase_regions(REGIONS_KEY)


if __name__ == "__main__":
	class MockLine(object):
		def __init__(self, line):
			self.complete_line = line

	class MockFileLines(object):
		def __init__(self, lines):
			self.all_lines = lines

	line1 = MockLine("function test(a) {")
	line2 = MockLine("	var b = 1 + 1;")
	line3 = MockLine("	alert(b);")
	line4 = MockLine("}")
	lines = MockFileLines([line1, line2, line3, line4])

	command = CleanjsCommand()
	assert command.get_points_from_line(3, lines) == (35,45)

	print "ALL TESTS OK"