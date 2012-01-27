import os

def run_unit_tests(dir):
	for item in os.listdir(dir):
		if item[-3:] == ".py" and item[0:8] != "cleanjs_" and item != "runtests.py" and item != "jsparser.py":
			os.system("python " + os.path.join(dir, item))

		try:
			run_unit_tests(os.path.join(dir, item))
		except:
			pass

def ensure_dir(dir_name):
	if not os.path.exists(dir_name):
		os.makedirs(dir_name)

def run_full_tests():
	script_dir = "scripts"
	report_dir = script_dir + os.sep + "reports"
	ensure_dir(report_dir)
	
	for item in os.listdir("scripts"):
		if item[-3:] == ".js":
			print "-- RUNNING CLEANJS ON " + item
			os.system("python .." + os.sep + "cleanjs_cmdline.py scripts" + os.sep + item + " " + report_dir + os.sep + item + "-report.html")

print ""
print "-- RUNNING ALL UNIT TETS"
run_unit_tests("..")

print ""
run_full_tests()