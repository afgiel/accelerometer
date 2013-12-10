import shutil
from os import listdir, path, mkdir

PATH = "../data/device_templates/"
DISC_BY = 1000

for f in listdir(PATH):
	if path.isfile(PATH + f):
		print f
		dID = int(f[2:len(f)-4])
		folderNum = dID//DISC_BY
		source = PATH + f
		print source
		dest = PATH + str(folderNum) + "/"
		if not (path.exists(dest) and path.isdir(dest)):
			mkdir(dest)
		try:
			shutil.move(source, dest)
			print "Success moving" + f + " to " + dest
		except:
			print "Error moving " + f + " to " + dest
		break