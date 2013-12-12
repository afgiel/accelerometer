"""
Project: Authenticating Smart Phone Users via Accelerometer Readings
Contributors: Andrew Giel, Jonathan NeCamp

Overview:
	Use a person's biometric as detected from accelerometer
readings to authenticate them as the user of their smart
phone.
"""
import csv
import stepDetection
import device
import argparse
import authentication
import selfTrainSelfTest
import os

RAW_DATA_PATH = "../data/raw/"
SEQ_DATA_PATH = "../data/sequence_data/"
DEVICE_DATA_PATH = "../data/device_data/"
SEQ_TEMP_PATH = "../data/sequence_templates/"
DEVICE_TEMPLATE_PATH = "../data/device_templates/"
DEVICE_DEV_PATH = "../data/device_dev/"
INITIAL_HIGH_DT = 300
D_HIGH_DT = 25

INITIAL_MIN_TIME = 30000
D_MIN_TIME = 2000

CYCLE_THRESHOLD = 10
D_CYCLE_THRESHOLD = 2

THRESHOLD_PERCENT = 1.03

CYCLE_THRESHOLD_IDX = 0
MIN_TIME_IDX = 1
HIGH_DT_IDX = 2

CONSTRAINTS_IT_DICT_FOR_DEV = {
	0: (CYCLE_THRESHOLD, INITIAL_MIN_TIME, INITIAL_HIGH_DT),
	1: (CYCLE_THRESHOLD, INITIAL_MIN_TIME - D_MIN_TIME, INITIAL_HIGH_DT),
	2: (CYCLE_THRESHOLD, INITIAL_MIN_TIME - 2*D_MIN_TIME, INITIAL_HIGH_DT),
	3: (CYCLE_THRESHOLD, INITIAL_MIN_TIME - 3*D_MIN_TIME, INITIAL_HIGH_DT),
	4: (CYCLE_THRESHOLD, INITIAL_MIN_TIME - 4*D_MIN_TIME, INITIAL_HIGH_DT),
	5: (CYCLE_THRESHOLD - D_CYCLE_THRESHOLD, INITIAL_MIN_TIME - 5*D_MIN_TIME, INITIAL_HIGH_DT),
	6: (CYCLE_THRESHOLD - D_CYCLE_THRESHOLD, INITIAL_MIN_TIME - 6*D_MIN_TIME, INITIAL_HIGH_DT + D_HIGH_DT),
	7: (CYCLE_THRESHOLD - 2*D_CYCLE_THRESHOLD, INITIAL_MIN_TIME - 7*D_MIN_TIME, INITIAL_HIGH_DT + 2*D_HIGH_DT),
	8: (CYCLE_THRESHOLD - 2*D_CYCLE_THRESHOLD, INITIAL_MIN_TIME - 8*D_MIN_TIME, INITIAL_HIGH_DT + 3*D_HIGH_DT),
	9: (CYCLE_THRESHOLD - 3*D_CYCLE_THRESHOLD, INITIAL_MIN_TIME - 9*D_MIN_TIME, INITIAL_HIGH_DT + 4*D_HIGH_DT),
	10: (CYCLE_THRESHOLD- 3*D_CYCLE_THRESHOLD, INITIAL_MIN_TIME - 10*D_MIN_TIME, INITIAL_HIGH_DT+ 5*D_HIGH_DT),
	11: (CYCLE_THRESHOLD- 4*D_CYCLE_THRESHOLD, INITIAL_MIN_TIME - 11*D_MIN_TIME, INITIAL_HIGH_DT+ 5*D_HIGH_DT),
	12: (CYCLE_THRESHOLD- 4*D_CYCLE_THRESHOLD, INITIAL_MIN_TIME - 11*D_MIN_TIME, INITIAL_HIGH_DT+ 6*D_HIGH_DT),
	13: (CYCLE_THRESHOLD- 4*D_CYCLE_THRESHOLD, INITIAL_MIN_TIME - 11*D_MIN_TIME, INITIAL_HIGH_DT+ 8*D_HIGH_DT),
	14: (CYCLE_THRESHOLD- 4*D_CYCLE_THRESHOLD, INITIAL_MIN_TIME - 11*D_MIN_TIME, INITIAL_HIGH_DT+ 10*D_HIGH_DT),
	15: (CYCLE_THRESHOLD- 4*D_CYCLE_THRESHOLD, INITIAL_MIN_TIME - 11*D_MIN_TIME, INITIAL_HIGH_DT+ 20*D_HIGH_DT),
	16: (CYCLE_THRESHOLD- 4*D_CYCLE_THRESHOLD, INITIAL_MIN_TIME - 11*D_MIN_TIME, INITIAL_HIGH_DT + 30*D_HIGH_DT),
	17: (CYCLE_THRESHOLD- 4*D_CYCLE_THRESHOLD, INITIAL_MIN_TIME - 11*D_MIN_TIME, INITIAL_HIGH_DT + 40*D_HIGH_DT),
	18: (CYCLE_THRESHOLD- 4*D_CYCLE_THRESHOLD, INITIAL_MIN_TIME - 11*D_MIN_TIME, INITIAL_HIGH_DT + 1000*D_HIGH_DT)
}

CYCLE_THRESHOLD_FOR_SEQ = 1
MIN_TIME_FOR_SEQ = 8000
INITIAL_HIGH_DT_FOR_SEQ = 350
D_HIGH_DT_FOR_SEQ = 50
MAX_SEQ_ITERATIONS = 6


CONSTRAINTS_IT_DICT_FOR_SEQ = {
	0: (CYCLE_THRESHOLD_FOR_SEQ, MIN_TIME_FOR_SEQ, INITIAL_HIGH_DT_FOR_SEQ),
	1: (CYCLE_THRESHOLD_FOR_SEQ, MIN_TIME_FOR_SEQ, INITIAL_HIGH_DT_FOR_SEQ + D_HIGH_DT_FOR_SEQ),
	2: (CYCLE_THRESHOLD_FOR_SEQ, MIN_TIME_FOR_SEQ, INITIAL_HIGH_DT_FOR_SEQ + 3*D_HIGH_DT_FOR_SEQ),
	3: (CYCLE_THRESHOLD_FOR_SEQ, MIN_TIME_FOR_SEQ, INITIAL_HIGH_DT_FOR_SEQ + 6*D_HIGH_DT_FOR_SEQ),
	4: (CYCLE_THRESHOLD_FOR_SEQ, MIN_TIME_FOR_SEQ, INITIAL_HIGH_DT_FOR_SEQ + 10*D_HIGH_DT_FOR_SEQ),
	5: (CYCLE_THRESHOLD_FOR_SEQ, MIN_TIME_FOR_SEQ, INITIAL_HIGH_DT_FOR_SEQ + 100*D_HIGH_DT_FOR_SEQ),
	6: (CYCLE_THRESHOLD_FOR_SEQ, MIN_TIME_FOR_SEQ, INITIAL_HIGH_DT_FOR_SEQ + 1000*D_HIGH_DT_FOR_SEQ)

}



zeroTemplates = list()




def extractTemplate(d, cycleThreshold, verbose = True):
	if verbose:
		print "	------Reading Complete------"
		print "	Preprocessing data from Device", str(d.ID) + "..."
	d.preProcessData()
	if verbose:
		print "	------Preprocessing Complete------"
		print "	Detecting cycles from Device", str(d.ID) + "..."
	d.detectCycles()			
	if verbose:
		print "	------Cycle Detection Complete------"
	if (len(d.cycles) < cycleThreshold):
		if verbose:
			print "	Only", len(d.cycles), "detected cycles" 
			print "	Restarting average cycle detection with lower constraints"
		return
	if verbose:
		print "	Detected ", len(d.cycles), "cycles"
		print "	Averaging cycles from Device", str(d.ID) + "..."	
	d.averageCycles()
	if verbose:
		print "	------Template Created------"


def writeTemplateToFile(d, templatePath, isDevice, verbose = True):
	prefix = "s_"
	if isDevice:
		prefix = "d_"
	if verbose:
		print "	Writing template to file for Device", str(d.ID) + "..."
	with open(templatePath + prefix + str(d.ID) + ".txt", "w") as templateFile:
		toWrite = str([x[1] for x in d.averageCycle])
		templateFile.write(toWrite)					
	if verbose:
		print "	------Template Written------"

def writeZeroTemplate(d, templatePath, verbose = True):
	if verbose:
		print "	Writing template to file for Device", str(d.ID) + "..."
	with open(templatePath + "s_" + str(d.ID) + ".txt", "w") as templateFile:
		toWrite = str([0 for x in xrange(120)])
		templateFile.write(toWrite)					
	if verbose:
		print "	------Template Written------"


def writeDevToFile(d, devPath, verbose =True):
	if verbose:
		print "	Writing develepment score to file for Device", str(d.ID) + "..."
	with open(devPath + "d_" + str(d.ID) + ".txt", "w") as devFile:
		toWrite = str(d.averageDevScore)
		devFile.write(toWrite)
	if verbose:
		print "	------Development Score Written------"
		print

def lowerConstraints(iteration, isDevice, verbose):
	newConstraints = tuple()
	if isDevice:
		newConstraints = CONSTRAINTS_IT_DICT_FOR_DEV[iteration]
	else: 
		newConstraints = CONSTRAINTS_IT_DICT_FOR_SEQ[iteration]
	if verbose:
		print "		Lowering constraints to:"
		print "			Minimum Time:", newConstraints[MIN_TIME_IDX]
		print "			High Upper bound of dt:", newConstraints[HIGH_DT_IDX]
		print "			Cycle Threshold:", newConstraints[CYCLE_THRESHOLD_IDX]
	return newConstraints

def createAndWriteTemplate(fileNamePath, templatePath, devPath, isDevice, verbose = True):
	detectedCycles = 0
	currentDevice = None
	iteration = 0
	cycleThreshold, minTime, highDT = lowerConstraints(iteration, isDevice, False)
	while (detectedCycles < cycleThreshold):
		if iteration != 0:
			cycleThreshold, minTime, highDT = lowerConstraints(iteration, isDevice, verbose)
		
		with open(fileNamePath, "r") as deviceData:
			currentDeviceID = int(next(deviceData))
			print "	Reading from device", str(currentDeviceID) + "..."
			deviceReader = csv.reader(deviceData)
			currentDevice = device.Device(currentDeviceID, 0.0, highDT, minTime)
			for sample in deviceReader:
				currentDevice.addSample(float(sample[0]), float(sample[1]), float(sample[2]), float(sample[3]))
		extractTemplate(currentDevice, cycleThreshold)
		detectedCycles = len(currentDevice.cycles)
		iteration += 1
		if not isDevice:	
			if iteration > MAX_SEQ_ITERATIONS:
				zeroTemplates.append(currentDevice.ID)
				writeZeroTemplate(currentDevice, templatePath)
				return

	writeTemplateToFile(currentDevice, templatePath, isDevice, True)
	if isDevice:
		writeDevToFile(currentDevice, devPath, True)


def createAllDeviceTemplates(verbose = True):
	if verbose:
		print("Training templates...")
		print
	for deviceFileName in os.listdir(DEVICE_DATA_PATH):
		deviceFileNamePath = os.path.join(DEVICE_DATA_PATH, deviceFileName)
		createAndWriteTemplate(deviceFileNamePath, DEVICE_TEMPLATE_PATH, DEVICE_DEV_PATH, True)


def createAllSequenceTemplates(verbose = True):
	if verbose:
		print "Creating Test Sequence Templates..."
		print 
	for x in xrange(1, 10):
		dirPath = SEQ_DATA_PATH+str(x)+"/"
		tempPath = SEQ_TEMP_PATH+str(x)+"/"
		for seqFileName in os.listdir(dirPath):
			seqFileNamePath = os.path.join(dirPath, seqFileName)
			createAndWriteTemplate(seqFileNamePath, tempPath, None, False)


def authenticate(questionFilename, numQuestions, verbose):
	if verbose:
		print "Authenticating..."
		print 
		print "Reading Questions..."
		print 
	questionList = list()
	with open(questionFilename) as questionData:
		next(questionData)
		questionReader = csv.reader(questionData)
		for question in questionReader:
			qID, sID, dID = question
			print qID, sID, dID
			# if (len(questionList)+ 1 > numQuestions):
			# 	break
			if verbose:
				print "	Reading device ", str(qID)+ "..."
			questionList.append((qID, sID, dID))
	answers = list()
	for question in questionList:
		prediction = authentication.authenticate(question)
		answers.append((question[0], prediction))
	with open("answers.crv", "w") as answerFile:
		for answer in answers:
			answerFile.write(str(answer[0]) + "," + str(answer[1]))




# Test

#authenticate("../data/raw/questions.csv", 10, True)
actions = ["train","createSequenceTemplates","createOneSequenceTemplate", "trainFromHalf", "testFromHalf", "authenticate", "both"]
booleans = [True, False]
parser = argparse.ArgumentParser(description = 'Process average gait cycle from accelerometer readings and authenticate user')
parser.add_argument("action", help = "train, authenticate, both", default = "train", choices = actions)
parser.add_argument("--verbose", help = "Prints out logging info when true", action = 'store_true')
parser.add_argument("--createTestTemps", help = "If test templates need to be created", action = 'store_true')
parser.add_argument("--numQuestions", help = "Number of questions to be asked to each device", type = int)
parser.add_argument("--threshold", help = "Number of questions to be asked to each device", type = float)
parser.add_argument("--justTotal", help = "Prints out just the total stats", action = 'store_true')
args = parser.parse_args()


if args.action == "train":
	createAllDeviceTemplates(args.verbose)

elif args.action == "createSequenceTemplates":
	createAllSequenceTemplates(args.verbose)
	print zeroTemplates

elif args.action == "createOneSequenceTemplate":
	path = "../data/sequence_data/1/seq_100197.csv"
	createAndWriteTemplate(path, None, None, False)

elif args.action == 'trainFromHalf':
	selfTrainSelfTest.trainFromHalf()

elif args.action == "testFromHalf":
	selfTrainSelfTest.testFromHalf(args.createTestTemps, args.threshold, args.numQuestions, args.justTotal)

elif args.action == "authenticate":
	createSequenceTemplate(args.testFile, 90024, args.verbose)
	authenticate("../data/questions.csv", 90024, args.verbose)
else:
	createAllTemplates(args.trainFile, args.numD, args.plot, args.verbose)
	authenticate("../data/questions.csv", 90024, args.verbose)

if args.verbose:
	print "All Done!"








