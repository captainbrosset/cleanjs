import os

def run_unit_tests(dir):
	for item in os.listdir(dir):
		if item[-3:] == ".py" and item[0:8] != "cleanjs_" and item != "runtests.py" and item != "jsparser.py":
			os.system("python " + os.path.join(dir, item))

		try:
			run_unit_tests(os.path.join(dir, item))
		except:
			pass

def run_full_tests():
	for item in os.listdir("scripts"):
		if item[-3:] == ".js":
			print "-- RUNNING CLEANJS ON " + item
			os.system("python ../cleanjs_cmdline.py scripts/" + item + " scripts/reports/" + item + "-report.html")

print ""
print "-- RUNNING ALL UNIT TETS"
run_unit_tests("..")

print ""
run_full_tests()