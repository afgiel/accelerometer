import csv
import device
import dtw
import linRegress
from os import listdir

TEMPLATE_PATH = "../data/device_templates/"
DEV_PATH = "../data/device_dev/"
TRAIN_ERROR_PATH = "../data/train_error/"
RAW_FILE = "../data/raw/train.csv"
THRESHOLD_PERCENT = 1.05

def getOneTemplate(path, templateFile):
	templateFile = open(path + templateFile)
	templateStr = next(templateFile)
	templateStr = templateStr[1:len(templateStr)-1]
	template = templateStr.split(",")
	template = [float(x) for x in template]
	return template

def getAllTemplates():
	allTemplates = dict()
	for templateFile in listdir(TEMPLATE_PATH):
		if templateFile.startswith("d_"):
			dID = int(templateFile[2:len(templateFile)-4])
			template = getOneTemplate(TEMPLATE_PATH, templateFile)
			allTemplates[dID] = template
	return allTemplates

def getAllDevices():
	deviceList = list()
	with open(RAW_FILE) as trainData:
		next(trainData)
		trainReader = csv.reader(trainData)
		lastIDRead = -1
		deviceIndex = -1
		for sample in trainReader:
			currentDevice = int(sample[4])
			if currentDevice != lastIDRead:
				if lastIDRead != -1:
					extractCycles(deviceList[deviceIndex])
				deviceIndex += 1
				deviceList.append(device.Device(currentDevice))
				lastIDRead = currentDevice
			deviceList[deviceIndex].addSample(float(sample[0]), float(sample[1]), float(sample[2]), float(sample[3]))
	extractCycles(deviceList[deviceIndex])
	return deviceList

def extractCycles(d):
	print "	------Reading Complete------"
	print "	Preprocessing data from device " + str(d.ID) + "..."
	d.preProcessData()
	print "	------Preprocessing Complete------"
	print "	Detecting cycles from device " + str(d.ID) + "..."	
	d.detectCycles()
	print "	------Cycle Detection Complete------"

def getLineForDev(dev):
	toReturn = list()
	for idx, score in enumerate(dev):
		toReturn.append(score)
		if idx != 0:
			toReturn[idx] += toReturn[idx-1]
	return toReturn

def writeIndivOutTrainError(dID, truePos, trueNeg, falsePos, falseNeg):
	total = truePos + trueNeg + falsePos + falseNeg
	fileToWrite = open(TRAIN_ERROR_PATH + "te_d_" + str(dID) + ".txt", "w+")
	fileToWrite.write(str(truePos) + "," + str(float(truePos)/total) + "\n")
	fileToWrite.write(str(trueNeg) + "," + str(float(trueNeg)/total) + "\n")
	fileToWrite.write(str(falsePos) + "," + str(float(falsePos)/total) + "\n")
	fileToWrite.write(str(falseNeg) + "," + str(float(falseNeg)/total) + "\n")
	fileToWrite.close()

def writeAllOutTrainError(truePos, trueNeg, falsePos, falseNeg):
	total = truePos + trueNeg + falsePos + falseNeg
	fileToWrite = open(TRAIN_ERROR_PATH + "CUMULATIVE.txt", "w+")
	fileToWrite.write(str(truePos) + "," + str(float(truePos)/total) + "\n")
	fileToWrite.write(str(trueNeg) + "," + str(float(trueNeg)/total) + "\n")
	fileToWrite.write(str(falsePos) + "," + str(float(falsePos)/total) + "\n")
	fileToWrite.write(str(falseNeg) + "," + str(float(falseNeg)/total) + "\n")
	fileToWrite.close()

def makePrediction(dTemplate, toTest, avgDev):
	disregard, testDev = dtw.getDTW(dTemplate, toTest)
	avgSlope = linRegress.getSlopeForDifference([i for i in range(len(avgDev))], avgDev)
	testSlope = linRegress.getSlopeForDifference([i for i in range(len(testDev))], testDev)
	return 1 if testSlope <= avgSlope*THRESHOLD_PERCENT else 0

def calculateTrainErrorForOne(device, templates):
	print "	Calculating train error for device " + str(device.ID) + "..."	
	dID = device.ID 
	toTest = set()
	dTemplate = templates[dID]
	avgDevelopmentScore = getOneTemplate(DEV_PATH, "d_" + str(dID) + ".txt")
	avgDev = getLineForDev(avgDevelopmentScore)
	for tupleCycle in device.cycles:
		cycle = [x[1] for x in tupleCycle]
		toTest.add((tuple(cycle), 1))
	for otherDevice in templates:
		if otherDevice != dID:
			toTest.add((tuple(templates[otherDevice]), 0))
	truePos = 0
	trueNeg = 0
	falsePos = 0
	falseNeg = 0
	for test in toTest:
		testAgainst = list(test[0])
		answer = test[1]
		prediction = makePrediction(dTemplate, testAgainst, avgDev)
		if prediction == answer:
			if answer == 0: 
				truePos += 1
			else:
				trueNeg += 1
		else:
			if answer == 0: 
				falsePos += 1
			else:
				falseNeg += 1
	writeIndivOutTrainError(dID, truePos, trueNeg, falsePos, falseNeg)
	return truePos, trueNeg, falsePos, falseNeg

def calculateTrainErrorForAll(devices, templates):
	truePos, trueNeg, falsePos, falseNeg = 0, 0, 0, 0
	for device in devices:
		indivTP, indivTN, indivFP, indivFN = calculateTrainErrorForOne(device, templates)
		truePos += indivTP
		trueNeg += indivTN
		falsePos += indivFP
		falseNeg += indivFN
	writeAllOutTrainError(truePos, trueNeg, falsePos, falseNeg)
	print "	------Train Error Complete------"

templates = getAllTemplates()
devices = getAllDevices()
calculateTrainErrorForAll(devices, templates)




