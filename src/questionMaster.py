"""
Documentation:


Assumptions:
	First question in question set should be true, all others
	should be false

"""

"""
"""

import random

TRAIN_DATA_PATH = "../data/train_data/"
TEST_DATA_PATH = "../data/test_data/"
STATS = ["Total Questions", "Total Correct", "True Positives", "True Negatives" ,
	"False Positives", "False Negatives"]
ALL_DEVICES_KEY = -1


def getRandomSample(source, numSamples, excludedDevice):
	randomSample = random.sample(source, numSamples +1)
	if excludedDevice in randomSample:
		randomSample.remove(excludedDevice)
	else:
		randomSample.remove(randomSample[0])
	return randomSample

def createStatsDict(deviceList):
	statsDict = dict()
	statsDict[ALL_DEVICES_KEY] = dict()
	for stat in STATS:
		statsDict[ALL_DEVICES_KEY][stat] = 0
	for device in deviceList:
		statsDict[device] = dict()
		for stat in STATS:
			statsDict[device][stat] = 0
	return statsDict

def getCorrectResponse(numQuestionsPerDevice):
	correctResponse = list()
	correctResponse.append(1)
	for _ in xrange(numQuestionsPerDevice - 1):
		correctResponse.append(0)
	return correctResponse


class QuestionMaster:
	"""


	"""


	def __init__(self, deviceList, numQuestionsPerDevice = 5, testPath = TEST_DATA_PATH):
		"""


		"""

		self.numQuestionsPerDevice = numQuestionsPerDevice
		self.testPath = testPath
		self.deviceList = deviceList
		self.stats = createStatsDict(self.deviceList)
		self.correctResponse = getCorrectResponse(numQuestionsPerDevice)



	def getQuestions(self, device):
		"""
		"""
		if device not in self.deviceList:
			return None

		else:
			questions = list()
			questions.append(self.testPath + "test_" + str(device))
			randomSample = getRandomSample(self.deviceList, self.numQuestionsPerDevice, device)
			for randomDevice in randomSample:
				questions.append(self.testPath + "test_" + str(randomDevice))
			return questions

	def answer(self, device, response):
		questions = correct = truePositives = trueNegatives = falsePositives = falseNegatives = 0
		for idx in xrange(len(response)):
			questions += 1
			if self.correctResponse[idx] == 0:
				if response[idx] == 0:
					correct += 1
					trueNegatives += 1
				else:
					falsePositives += 1
			else:
				if response[idx] == 0:
					falseNegatives += 1
				else:
					correct += 1
					truePositives += 1
		self.updateStats(device, questions, correct, truePositives, trueNegatives, falsePositives, falseNegatives)

	def updateStats(self, device, questions, correct, truePositives, trueNegatives, falsePositives, falseNegatives):
		self.stats[device]["Total Questions"] += questions
		self.stats[ALL_DEVICES_KEY]["Total Questions"] += questions

		self.stats[device]["Total Correct"] += correct
		self.stats[ALL_DEVICES_KEY]["Total Correct"] += correct

		self.stats[device]["True Positives"] += truePositives
		self.stats[ALL_DEVICES_KEY]["True Positives"] += truePositives

		self.stats[device]["True Negatives"] += trueNegatives
		self.stats[ALL_DEVICES_KEY]["True Negatives"] += trueNegatives

		self.stats[device]["False Positives"] += falsePositives
		self.stats[ALL_DEVICES_KEY]["False Positives"] += falsePositives

		self.stats[device]["False Negatives"] += falseNegatives
		self.stats[ALL_DEVICES_KEY]["False Negatives"] += falseNegatives


	def printStatsForDevice(self, device):
		print "-----DEVICE", device, "STATS-----"
		print "Total Questions:", self.stats[device]["Total Questions"]
		print "Total Correct:", self.stats[device]["Total Correct"]
		print "Accuracy:", float(self.stats[device]["Total Correct"]) / self.stats[device]["Total Questions"] *100, "%"
		print "True Positives:", self.stats[device]["True Positives"]
		print "True Negatives:", self.stats[device]["True Negatives"]
		print "False Positives:", self.stats[device]["False Positives"]
		print "False Negatives:", self.stats[device]["False Negatives"]

	def printTotalStats(self):
		print "----TOTAL STATS----"
		print "Total Questions:", self.stats[ALL_DEVICES_KEY]["Total Questions"]
		print "Total Correct:", self.stats[ALL_DEVICES_KEY]["Total Correct"]
		print "Accuracy:", float(self.stats[ALL_DEVICES_KEY]["Total Correct"]) / self.stats[ALL_DEVICES_KEY]["Total Questions"] *100, "%"
		print "True Positives:", self.stats[ALL_DEVICES_KEY]["True Positives"]
		print "True Negatives:", self.stats[ALL_DEVICES_KEY]["True Negatives"]
		print "False Positives:", self.stats[ALL_DEVICES_KEY]["False Positives"]
		print "False Negatives:", self.stats[ALL_DEVICES_KEY]["False Negatives"]
