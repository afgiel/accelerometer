"""
Project: User Authentication With Gait Biometric
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

RAW_DATA_PATH = "../data/raw/"
SEQ_TEMP_PATH = "../data/sequence_templates/"
DEV_TEMP_PATH = "../data/device_templates/"
DEV_DEV_PATH = "../data/device_dev/"

# Create template

interval = 100


def createTemplate(filename, numDevices, toPlot, verbose):
	if verbose:
		print("Training templates...")
		print
	deviceList = list()
	with open(filename) as trainData:
		next(trainData)
		trainReader = csv.reader(trainData)
		lastIDRead = -1
		deviceIndex = -1
		for sample in trainReader:
			currentDevice = int(sample[4])
			if currentDevice != lastIDRead:
				if (len(deviceList)+ 1 > numDevices):
					break
				if verbose:
					print "	Reading device ", str(currentDevice)+ "..."
				deviceIndex += 1
				deviceList.append(device.Device(currentDevice))
				lastIDRead = currentDevice
			deviceList[deviceIndex].addSample(float(sample[0]), float(sample[1]), float(sample[2]), float(sample[3]))
	if verbose:
		print "	------Reading Complete------"
		print



	for d in deviceList:
		if verbose:
			print "	Preprocessing data from device", str(d.ID) + "..."
		d.preProcessData()
	if verbose:
		print "	------Preprocessing Complete------"
		print

	# for d in deviceList:
	# 	if verbose:
	# 		print str(d.ID), "Most common difference in time between readings"
	# 		print "	", d.timeDifferences.most_common(20)

	for d in deviceList:
		if verbose:
			print "	Detecting cycles from device", str(d.ID) + "..."
		d.detectCycles()
	if verbose:
		print "	------Cycle Detection Complete------"
		print

	for d in deviceList:
		print str(d.ID), len(d.cycles)

	for d in deviceList:
		if verbose:
			print "	Averaging cycles from device", str(d.ID) + "..."
		d.averageCycles()
	if verbose:
		print "	------Templates Created------"
		print

	for d in deviceList:
		if verbose:
			print "	Writing template to file for device", str(d.ID) + "..."
		with open(DEV_TEMP_PATH + "d_" + str(d.ID) + ".txt", "w") as templateFile:
			toWrite = str(d.averageCycle)
			templateFile.write(toWrite)
	if verbose:
		print "	------Templates Written------"

	for d in deviceList:
		if verbose:
			print "	Writing develepment score to file for device", str(d.ID) + "..."
		with open(DEV_DEV_PATH + "d_" + str(d.ID) + ".txt", "w") as devFile:
			toWrite = str(d.averageDevScore)
			devFile.write(toWrite)
	if verbose:
		print "	------Development Score Written------"

	if toPlot:
		deviceList[0].plotData()

def createSequenceTemplate(testFilename, numSequences,verbose):
	if verbose:
		print "Reading Test Sequences..."
		print 
	sequenceList = list()
	with open(testFilename) as testData:
		next(testData)
		testReader = csv.reader(testData)
		lastSIDRead = -1
		sequenceIndex = -1
		for sample in testReader:
			currentSequence = int(sample[4])
			if currentSequence != lastSIDRead:
				if (len(sequenceList)+ 1 > numSequences):
					break
				if verbose:
					print "	Reading sequence ", str(currentSequence)+ "..."
				sequenceIndex += 1
				sequenceList.append(device.Device(currentSequence))
				lastSIDRead = currentSequence
			sequenceList[sequenceIndex].addSample(float(sample[0]), float(sample[1]), float(sample[2]), float(sample[3]))
	if verbose:
		print "	------Reading Complete------"
		print

	for s in sequenceList:
		if verbose:
			print "	Preprocessing data from sequence", str(s.ID) + "..."
		s.preProcessData()
	if verbose:
		print "	------Preprocessing Complete------"
		print



	for s in sequenceList:
		if verbose:
			print "	Detecting cycles from sequence", str(s.ID) + "..."
		s.detectCycles()
	if verbose:
		print "	------Cycle Detection Complete------"
		print



	for s in sequenceList:
		if verbose:
			print "	Averaging cycles from sequence", str(s.ID) + "..."
		s.averageCycles()
	if verbose:
		print "	------Templates Created------"
		print

	for s in sequenceList:
		if verbose:
			print "	Writing template to file for sequence", str(s.ID) + "..."
		with open(SEQ_TEMP_PATH + "s_" + str(s.ID) + ".txt", "w") as templateFile:
			toWrite = str(s.averageCycle)
			templateFile.write(toWrite)
	if verbose:
		print "	------Templates Written------"


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
			# if (len(questionList)+ 1 > numQuestions):
			# 	break
			if verbose:
				print "	Reading device ", str(qID)+ "..."
			questionList.append((qId, sID, dID))
	answers = list()
	for question in questionList:
		prediction = authentication.authenticate(question)
		answers.append((question[0], prediction))
	with open("answers.crv", "w") as answerFile:
		for answer in answers:
			answerFile.write(str(answer[0]) + "," + str(answer[1]))




# Test


actions = ["train", "authenticate", "both"]
booleans = [True, False]
parser = argparse.ArgumentParser(description = 'Process average gait cycle from accelerometer readings and authenticate user')
parser.add_argument("action", help = "train, authenticate, both", default = "train", choices = actions)
parser.add_argument("--TDfile", help = "File where data to train authenticator is stored", default = "../data/raw/train.csv")
parser.add_argument("--tempFile", help = "File where templates are stored")
parser.add_argument("--numD", help = "Number of devices to create templates for", type = int, default = 400)
parser.add_argument("--plot", help = "Boolean indicating whether data should be plotted", default = False, choices= booleans, type = bool)
parser.add_argument("--verbose", help = "Prints out logging info when true", choices = booleans, default = True)
args = parser.parse_args()


if args.action == "train":
	createTemplate(args.TDfile, args.numD, args.plot, args.verbose)
elif args.action == "authenticate":
	authenticate()
else:
	createTemplate(args.TDfile, args.numD, args.plot, args.verbose)
	authenticate("../data/questions.csv", 90024, args.verbose)

if args.verbose:
	print "All Done!"








