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

RAW_DATA_PATH = "../data/raw/"
SEQ_TEMP_PATH = "../data/sequence_templates/"
DEV_TEMP_PATH = "../data/device_templates/"
DEV_DEV_PATH = "../data/device_dev/"

# Create template

interval = 100


zeroCycleDevices = list()


def extractTemplate(d, verbose, string):
	if verbose:
		print "	------Reading Complete------"
		print "	Preprocessing data from", string, str(d.ID) + "..."
	d.preProcessData()
	if verbose:
		print "	------Preprocessing Complete------"
		print "	Detecting cycles from", string, str(d.ID) + "..."
	d.detectCycles()			
	if verbose:
		print "	------Cycle Detection Complete------"
		print
		print "	", string, str(d.ID), "detected", len(d.cycles), "cycles"
		print
	if len(d.cycles) == 0:
		zeroCycleDevices.append(d.ID)
	if verbose:
		print "	Averaging cycles from", string, str(d.ID) + "..."
	d.averageCycles()
	if verbose:
		print "	------Templates Created------"
		print "	Writing template to file for", string, str(d.ID) + "..."
	if string == "Sequence":
		with open(SEQ_TEMP_PATH + "s_" + str(d.ID) + ".txt", "w") as templateFile:
			toWrite = str([x[1] for x in d.averageCycle])
			templateFile.write(toWrite)
		if verbose:
			print "	------Templates Written------"
			print
	else:
		with open(DEV_TEMP_PATH + "d_" + str(d.ID) + ".txt", "w") as templateFile:
			toWrite = str([x[1] for x in d.averageCycle])
			templateFile.write(toWrite)					
		if verbose:
			print "	------Templates Written------"
			print "	Writing develepment score to file for", string, str(d.ID) + "..."
		with open(DEV_DEV_PATH + "d_" + str(d.ID) + ".txt", "w") as devFile:
			toWrite = str(d.averageDevScore)
			devFile.write(toWrite)
		if verbose:
			print "	------Development Score Written------"
			print

def createOneTemplate(filename, deviceID, toPlot, verbose):
	if verbose:
		print "Training template for Device", deviceID
		print
	with open(filename) as trainData:
		next(trainData)
		trainReader = csv.reader(trainData)
		d = device.Device(deviceID)
		print "* Reading device ", str(deviceID)+ "..."
		startedReading = False
		for sample in trainReader:
			if int(sample[4]) == deviceID:
				startedReading = True
				d.addSample(float(sample[0]), float(sample[1]), float(sample[2]), float(sample[3]))
			elif startedReading:
				break
		extractTemplate(d, verbose, "Device")
		print "Number of samples read for device", deviceID, ":", d.numSamples

def createListsTemplate(filename, deviceIDList, toPlot, verbose):
	if verbose:
		print "Training templates"
		print
	with open(filename) as trainData:
		next(trainData)
		trainReader = csv.reader(trainData)
		currentIDx = 0
		print "* Reading device ", str(deviceIDList[currentIDx])+ "..."
		d = device.Device(deviceIDList[currentIDx])
		startedReading = False
		for sample in trainReader:
			if int(sample[4]) == deviceIDList[currentIDx]:
				startedReading = True
				d.addSample(float(sample[0]), float(sample[1]), float(sample[2]), float(sample[3]))
			elif startedReading:
				extractTemplate(d, verbose, "Device")
				currentIDx += 1
				if currentIDx == len(deviceIDList):
					break
				print "* Reading device ", str(deviceIDList[currentIDx])+ "..."
				d = device.Device(deviceIDList[currentIDx])
				startedReading = False
				


def createAllTemplates(filename, numDevices, toPlot, verbose):
	if verbose:
		print("Training templates...")
		print
	deviceList = list()
	with open(filename) as trainData:
		next(trainData)
		trainReader = csv.reader(trainData)
		lastIDRead = -1
		deviceIndex = -1
		exceedNumDevicesFlag = False
		for sample in trainReader:
			currentDevice = int(sample[4])
			if currentDevice != lastIDRead:
				if lastIDRead != -1:
					extractTemplate(deviceList[deviceIndex], verbose, "Device")
				if (len(deviceList)+ 1 > numDevices):
					exceedNumDevicesFlag = True
					break
				if verbose:
					print "* Reading device ", str(currentDevice)+ "..."
				deviceIndex += 1
				deviceList.append(device.Device(currentDevice))
				lastIDRead = currentDevice
			deviceList[deviceIndex].addSample(float(sample[0]), float(sample[1]), float(sample[2]), float(sample[3]))
		if not exceedNumDevicesFlag:
			extractTemplate(deviceList[deviceIndex], verbose, "Device")

	if toPlot:
		deviceList[0].plotData()



def createSequenceTemplateAfter(testFilename, numSequences, verbose):
	if verbose:
		print "Reading Test Sequences..."
		print 
	sequenceList = list()
	with open(testFilename) as testData:
		next(testData)
		testReader = csv.reader(testData)
		lastSIDRead = -1
		sequenceIndex = -1
		exceedNumSequencesFlag = False
		for sample in testReader:
			currentSequence = int(sample[4])
			if int(sample[4]) > numSequences:
				if currentSequence != lastSIDRead:
					if lastSIDRead != -1:
						extractTemplate(sequenceList[sequenceIndex], verbose, "Sequence")
					# if (len(sequenceList)+ 1 > numSequences):
					# 	exceedNumSequencesFlag = True
					# 	break
					if verbose:
						print "* Reading sequence ", str(currentSequence)+ "..."
					sequenceIndex += 1
					sequenceList.append(device.Device(currentSequence))
					lastSIDRead = currentSequence
				sequenceList[sequenceIndex].addSample(float(sample[0]), float(sample[1]), float(sample[2]), float(sample[3]))
		if not exceedNumSequencesFlag:
			extractTemplate(sequenceList[sequenceIndex], verbose, "Sequence")


def createSequenceTemplate(testFilename, numSequences, verbose):
	if verbose:
		print "Reading Test Sequences..."
		print 
	sequenceList = list()
	with open(testFilename) as testData:
		next(testData)
		testReader = csv.reader(testData)
		lastSIDRead = -1
		sequenceIndex = -1
		exceedNumSequencesFlag = False
		for sample in testReader:
			currentSequence = int(sample[4])
			if currentSequence != lastSIDRead:
				if lastSIDRead != -1:
					extractTemplate(sequenceList[sequenceIndex], verbose, "Sequence")
				if (len(sequenceList)+ 1 > numSequences):
					exceedNumSequencesFlag = True
					break
				if verbose:
					print "* Reading sequence ", str(currentSequence)+ "..."
				sequenceIndex += 1
				sequenceList.append(device.Device(currentSequence))
				lastSIDRead = currentSequence
			sequenceList[sequenceIndex].addSample(float(sample[0]), float(sample[1]), float(sample[2]), float(sample[3]))
		if not exceedNumSequencesFlag:
			extractTemplate(sequenceList[sequenceIndex], verbose, "Sequence")



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
actions = ["train", "train1", "trainList", "trainFromHalf", "testFromHalf", "authenticate", "authenticateAfter", "both"]
booleans = [True, False]
parser = argparse.ArgumentParser(description = 'Process average gait cycle from accelerometer readings and authenticate user')
parser.add_argument("action", help = "train, authenticate, both", default = "train", choices = actions)
parser.add_argument("--trainFile", help = "File where data to train authenticator is stored", default = "../data/raw/train.csv")
parser.add_argument("--testFile", help = "File where data to create templates for tests is stored", default = "../data/raw/test.csv")
parser.add_argument("--tempFile", help = "File where templates are stored")
parser.add_argument("--numD", help = "Number of devices to create templates for", type = int, default = 400)
parser.add_argument("--plot", help = "Boolean indicating whether data should be plotted", default = False, choices= booleans, type = bool)
parser.add_argument("--verbose", help = "Prints out logging info when true", choices = booleans, default = True)
parser.add_argument("--device", help = "Single device ID to create template for", type = int)
args = parser.parse_args()


if args.action == "train":
	createAllTemplates(args.trainFile, args.numD, args.plot, args.verbose)
	print zeroCycleDevices

elif args.action == "train1":
	createOneTemplate(args.trainFile, args.device, args.plot, args.verbose)

elif args.action == 'trainFromHalf':
	selfTrainSelfTest.trainFromHalf()

elif args.action == "testFromHalf":
	selfTrainSelfTest.testFromHalf()

elif args.action == "trainList":
	devices = [401, 537]
	createListsTemplate(args.trainFile, devices, args.plot, args.verbose)
	print zeroCycleDevices

elif args.action == "authenticateAfter":
	createSequenceTemplateAfter(args.testFile, 700000, args.verbose)

elif args.action == "authenticate":
	createSequenceTemplate(args.testFile, 90024, args.verbose)
	authenticate("../data/questions.csv", 90024, args.verbose)
else:
	createAllTemplates(args.trainFile, args.numD, args.plot, args.verbose)
	authenticate("../data/questions.csv", 90024, args.verbose)

if args.verbose:
	print "All Done!"








