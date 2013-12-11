"""
Documentation:
	Splits the raw data into to subsets: one that will
	be used for training, another for testing.  It adds
	a file for each device into a training directory and
	a testing directory where is each file is exactly half
	of the raw data associated with that device.

Assumptions:
	First sequence is sequence 100006
	File paths will not be changed
	First device is always device 7.
	First line in data in useless
"""

import csv


RAW_TRAIN_DATA_PATH = "../data/raw/train.csv"
RAW_TEST_DATA_PATH = "../data/raw/test.csv"
SEQUENCE_DATA_PATH = "../data/sequence_data/"
TRAIN_DATA_PATH = "../data/train_data/"
TEST_DATA_PATH = "../data/test_data/"
SEQUENCE_BASE = 100000


def createCSVLine(strTup):
	return strTup[0] + "," + strTup[1] + "," + \
		strTup[2] + "," + strTup[3] + "\n"





def splitSequenceDataIntoSubFiles(rawDataFile, sequenceDataPath):

	def writeSequenceDataFile(ID, dataList):
		with open(sequenceDataPath + str(ID / SEQUENCE_BASE)+ "/" + "seq_" + str(ID) + ".csv", "w") as trainFile:
			trainFile.write(str(ID) + "\n")
			for sample in dataList:
				trainFile.write(createCSVLine(sample))


	with open(rawDataFile) as data:
		next(data)
		dataReader = csv.reader(data)
		currentSequenceDataList = list()
		previousSequenceID = 100006
		for sample in dataReader:
			if (previousSequenceID == int(sample[4])):
				currentSequenceDataList.append(sample)
			else:
				writeSequenceDataFile(previousSequenceID, currentSequenceDataList)
				currentSequenceDataList = list()
				previousSequenceID = int(sample[4])
				currentSequenceDataList.append(sample)

		if len(previousSequenceID) > 0:
			writeTrainAndTestFiles(previousSequenceID, currentSequenceDataListd)


def splitDataInHalf(rawDataFile, trainPath, testPath):

	def writeTrainAndTestFiles(device, dataList):

		splitPoint = len(dataList)/2

		with open(trainPath + "train_" + str(device) + ".csv", "w") as trainFile:
			trainFile.write(str(device) + "\n")
			for idx in xrange(splitPoint):
				trainFile.write(createCSVLine(dataList[idx]))

		with open(testPath + "test_" + str(device) + ".csv", "w") as testFile:
			testFile.write(str(device) + "\n")
			for idx in xrange(splitPoint, len(dataList)):
				testFile.write(createCSVLine(dataList[idx]))

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


splitDataInHalf(RAW_TRAIN_DATA_PATH, TRAIN_DATA_PATH, TEST_DATA_PATH)
# splitSequenceDataIntoSubFiles(RAW_TEST_DATA_PATH, SEQUENCE_DATA_PATH)


