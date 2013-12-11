"""
Documentation:
	Splits the raw data into to subsets: one that will
	be used for training, another for testing.  It adds
	a file for each device into a training directory and
	a testing directory where is each file is exactly half
	of the raw data associated with that device.

Assumptions:
	File paths will not be changed
	First device is always device 7.
	First line in data in useless
"""

import csv


RAW_DATA_PATH = "../data/raw/train.csv"
TRAIN_DATA_PATH = "../data/train_data/"
TEST_DATA_PATH = "../data/test_data/"



def splitData(rawDataFile, trainPath, testPath):

	def createCSVLine(strTup):
		return strTup[0] + "," + strTup[1] + "," + \
					strTup[2] + "," + strTup[3] + "\n"

	def writeTrainAndTestFiles(previousDevice, currentDeviceDataList):

		splitPoint = len(currentDeviceDataList)/2

		with open(trainPath + "train_" + str(previousDevice) + ".csv", "w") as trainFile:
			for idx in xrange(splitPoint):
				trainFile.write(createCSVLine(currentDeviceDataList[idx]))

		with open(testPath + "test" + str(previousDevice) + ".csv", "w") as testFile:
			for idx in xrange(splitPoint, len(currentDeviceDataList)):
				testFile.write(createCSVLine(currentDeviceDataList[idx]))


	with open(rawDataFile) as data:
		next(data)
		dataReader = csv.reader(data)
		currentDeviceDataList = list()
		previousDevice = 7
		for sample in dataReader:
			if (previousDevice == int(sample[4])):
				currentDeviceDataList.append(sample)
			else:
				writeTrainAndTestFiles(previousDevice, currentDeviceDataList)
				currentDeviceDataList = list()
				previousDevice = int(sample[4])
				currentDeviceDataList.append(sample)

		if len(currentDeviceDataList) > 0:
			writeTrainAndTestFiles(previousDevice, currentDeviceDataList)



splitData(RAW_DATA_PATH, TRAIN_DATA_PATH, TEST_DATA_PATH)


