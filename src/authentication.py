import dtw
import linRegress
import matplotlib.pyplot as plt

SEQ_TEMP_PATH = "../data/sequence_templates/"
DEV_TEMP_PATH = "../data/device_templates/"
DEV_DEV_PATH = "../data/device_dev/"

SEQ_BASE = 100000

THRESHOLD_PERCENT = 1.03

def getTemplate(fileName):
	with open(fileName) as templateFile:
		templateStr = next(templateFile)
	templateStr = templateStr[1:len(templateStr)-1]
	template = templateStr.split(',')
	template = [float(x) for x in template]
	return template

def getLineForDev(dev):
	toReturn = list()
	for idx, score in enumerate(dev):
		toReturn.append(score)
		if idx != 0:
			toReturn[idx] += toReturn[idx-1]
	return toReturn

def getFileNamePath(ID, path, prefix):
	if prefix == "d_":
		return path + prefix + str(ID) + ".txt"
	else:
		return path + str(int(ID)/SEQ_BASE) + "/" + prefix + str(ID) + ".txt"

def authenticate(sID, dID):
	deviceTemplate = getTemplate(getFileNamePath(dID, DEV_TEMP_PATH, "d_"))
	sequenceTemplate = getTemplate(getFileNamePath(sID, SEQ_TEMP_PATH, "s_"))
	avgDevelopmentScore = getTemplate(getFileNamePath(dID, DEV_DEV_PATH, "d_"))
	dtwScore, seqDev = dtw.getDTW(deviceTemplate, sequenceTemplate)
	avgDev = getLineForDev(avgDevelopmentScore)
	seqDev = getLineForDev(seqDev)
	# plt.plot([i for i in range(len(deviceTemplate))], deviceTemplate, color='blue')
	# plt.plot([i for i in range(len(sequenceTemplate))], sequenceTemplate, color='red')
	# plt.plot([i for i in range(len(avgDev))], avgDev, color='blue')
	# plt.plot([i for i in range(len(seqDev))], seqDev, color='red')
	# plt.show()
	avgSlope = linRegress.getSlopeForDifference([i for i in range(len(avgDev))], avgDev)
	seqSlope = linRegress.getSlopeForDifference([i for i in range(len(seqDev))], seqDev)
	return 1 if seqSlope <= avgSlope*THRESHOLD_PERCENT else 0
