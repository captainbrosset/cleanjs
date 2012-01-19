import os

def test_all(dir):
	for item in os.listdir(dir):
		if item[-3:] == ".py" and item[0:8] != "cleanjs_" and item != "runtests.py" and item != "jsparser.py":
			os.system("python " + os.path.join(dir, item))

		try:
			test_all(os.path.join(dir, item))
		except:
			pass

test_all("..")