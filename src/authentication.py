import dtw
import linRegress


SEQ_TEMP_PATH = "../data/sequence_templates/"
DEV_TEMP_PATH = "../data/device_templates/"
DEV_DEV_PATH = "../data/device_dev/"

THRESHOLD_PERCENT = 1.05

def getTemplate(ID, path, prefix):
	filename = path + prefix + str(ID) + ".txt"
	with open(filename) as templateFile:
		templateStr = next(templateFile)
	templateStr = templateStr[1:len(templateStr)-1]
	template = templateStr.split(',')
	template = [float(x) for x in template]
	return template

def getLineForDev(dev):
	toReturn = list()
	for idx, score in dev:
		toReturn[idx] = score
		if idx != 0:
			toReturn[idx] += toReturn[idx-1]
	return toReturn


def authenticate(question):
	qID, sID, dID = question
	deviceTemplate = getTemplate(dID, DEV_TEMP_PATH, "d_")
	sequenceTemplate = getTemplate(sID, SEQ_TEMP_PATH, "s_")
	avgDevelopmentScore = getTemplate(dID, DEV_DEV_PATH, "d_")
	dtwScore, seqDev = dtw.getDTW(deviceTemplate, sequenceTemplate)
	avgDev = getLineForDev(avgDevelopmentScore)
	seqDev = getLineForDev(seqDev)
	avgSlope = linRegress.getSlopeForDifference([i for i in range(len(avgDev))], avgDev)
	seqSlope = linRegress.getSlopeForDifference([i for i in range(len(seqDev))], seqDev)
	return 1 if seqSlope <= avgSlope*THRESHOLD_PERCENT else 0