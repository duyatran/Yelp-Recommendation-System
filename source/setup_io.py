import os
import macros as m
# try to open the file specified by the given filename
def openFile(filename, mode):
	try:
		return open(filename, mode)
	except IOError:
		print "Couldn't open '" + filename + "'!"
		exit(1)

# ensure the given directory exists
def ensureDir(directory):
	if directory[-1] == '/':
		directory = directory[:-1]
	if not os.path.exists(directory):
		os.makedirs(directory)
	return directory

# try to cast the given value to an integer
def toInt(val):
	try:
		val = int(val)
	except ValueError:
		print "'" + val + "' is not an integer!"
		exit(2)
	return val

# try to cast the given value to a float
def toFlo(val):
	try:
		val = float(val)
	except ValueError:
		print "'" + val + "' is not a number!"
		exit(2)
	return val



def create_output_folders():
    print "Creating folders if necessary...",
    ensureDir(m.out_dir)
    ensureDir(m.out_dir)
    ensureDir(m.out_dir_original)
    ensureDir(m.out_dir_item_based)
    ensureDir(m.out_dir_potential)
<<<<<<< HEAD
    ensureDir(m.out_dir_users)
=======
    ensureDir(m.out_dir_users)
    ensureDir(m.out_dir_results)
    print "Done"
>>>>>>> 5ed87cdb9f932f73f87cc457c1d68f52be10f2fb
