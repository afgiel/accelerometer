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


# Create template

interval = 100


def createTemplate(file, numDevices, toPlot, verbose):
	if verbose:
		print("Training templates...")
		print
	deviceList = list()
	with open(file) as trainData:
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



	for d in deviceList:
		if verbose:
			print "	Detecting cycles from device", str(d.ID) + "..."
		d.detectCycles()
	if verbose:
		print "	------Cycle Detection Complete------"
		print



	for d in deviceList:
		if verbose:
			print "	Averaging cycles from device", str(d.ID) + "..."
		d.averageCycles()
	if verbose:
		print "	------Templates Created------"
		print




	if toPlot:
		deviceList[0].plotData()




def authenticate():
	if verbose:
		print "Authenticating..."
	return





# Test


actions = ["train", "authenticate", "both"]
booleans = [True, False]
parser = argparse.ArgumentParser(description = 'Process average gait cycle from accelerometer readings and authenticate user')
parser.add_argument("action", help = "train, authenticate, both", default = "train", choices = actions)
parser.add_argument("--TDfile", help = "File where data to train authenticator is stored", default = "train1.csv")
parser.add_argument("--tempFile", help = "File where templates are stored")
parser.add_argument("--numD", help = "Number of devices to create templates for", type = int, default = 1)
parser.add_argument("--plot", help = "Boolean indicating whether data should be plotted", default = False, choices= booleans, type = bool)
parser.add_argument("--verbose", help = "Prints out logging info when true", choices = booleans, default = True)
args = parser.parse_args()


if args.action == "train":
	createTemplate(args.TDfile, args.numD, args.plot, args.verbose)
elif args.action == "authenticate":
	authenticate()
else:
	createTemplate(args.TDfile, args.numD, args.plot, args.verbose)
	authenticate()

if args.verbose:
	print "All Done!"








