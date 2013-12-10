
import preProcess
import stepDetection
# import matplotlib.pyplot as plt
import numpy
import collections
import dtw
import random
import matplotlib.pyplot as plt

NUM_SAMPLES = 20


def getTimeDifference(dataList):
	if len(dataList) == 0:
		return 0
	else:
		return  dataList[len(dataList)-1][0] - dataList[0][0]

class Device:
	"""
	Class that stores all the information to create a
	template.


	Considerations:
	Adding more stats on read in data such as average dt

	"""

	def __init__(self, deviceID, lowDT = 0.0, highDT = 600, minSampleTime = 7000):
		"""


		"""

		self.ID = deviceID
		self.prevTime = None
		self.highDT = highDT
		self.lowDT = lowDT
		self.currIdx = 0
		self.minSampleTime = minSampleTime
		self.rawData = list()
		self.rawData.append(list())
		self.processedData = list()
		self.timeDifferences = collections.Counter()
		self.numSamples = 0

	



	def addSample(self, time, x, y, z):
		"""
		Takes in a time, x acceleration, y acc., z acc. tuple
		and adds it to the current sequence of readings if the following
		condition is met:
			-The change in time from the last reading falls within the range
			of expected time differences
		If the condition is not met, if there are enough samples in the current
		sequence to accurately to get a cycle template then the old sequence is
		kept and a new sequence will begin upon the next added sample.  If there
		are not enough samples in the current sequence, then the current sequence
		is scrapped and a new one will begin upond the next added sample.
		When the sample is added, the resultant acceleration is automatically found.
		"""
		self.numSamples += 1
		if self.prevTime != None:
			dt = abs(time - self.prevTime)
			self.timeDifferences[dt] += 1
			if dt > self.highDT:
				if getTimeDifference(self.rawData[self.currIdx]) >= self.minSampleTime:
					self.currIdx += 1
					self.rawData.append(list())
				else:
					self.rawData[self.currIdx] = list()
				
			else: 
				self.rawData[self.currIdx].append(preProcess.resultantAcceleration(time, x, y, z))
		self.prevTime = time
		

	def preProcessData(self, interval = 10, window = 5):
		"""

		"""
		#Takes care of edge case where the last sequence is not
		#large enough to accurately create a template.
		if getTimeDifference(self.rawData[self.currIdx]) < self.minSampleTime:
			self.rawData.pop(self.currIdx)

		for idx, seq in enumerate(self.rawData):
			self.processedData.append(preProcess.linearInterpolation(interval, seq))
			preProcess.WeightedMovingAverage(self.processedData[idx], window)


	def plotData(self):
		"""
		"""
		# t = []
		# r = []
		# for ti,ri in self.processedData[0]:
		# 	t.append(ti)
		# 	r.append(ri)
		# plt.plot(t, r)
		return

	def detectCycles(self):
		"""

		"""
		self.cycles = list()
		for idx, seq in enumerate(self.processedData):
			cl = stepDetection.getAverageCycleLength(seq)
			minVal = stepDetection.getEstimateOfMin(seq, cl)
			si = stepDetection.getStartIndex(seq, cl)
			stepDetection.detectAllCycles(self.cycles, seq, cl, minVal, si)

	def averageDevAgainstTemplate(self, devScores):
		avgDevScore = list()
		allScores = dict()
		for devScore in devScores:
			for idx, score in enumerate(devScore):
				if idx not in allScores:
					allScores[idx] = list()
				allScores[idx].append(score)
		for idx in allScores:
			indexScore = allScores[idx]
			avgForIndex = numpy.mean(indexScore)
			avgDevScore.append(avgForIndex)
		self.averageDevScore = avgDevScore

	def averageCycles(self):
		totalDistances = list()
		devScores = dict()
		precomputed = dict()
		samples = list()
		if len(self.cycles) < NUM_SAMPLES:
			samples = self.cycles
		else:
			samples = random.sample(self.cycles, NUM_SAMPLES)
		for sample in samples:
			plt.plot([i for i in range(len(sample))], [x[1] for x in sample], color='orange')
			# print [x[1] for x in sample], "\n\n\n\n------"
		for idx1, cycle in enumerate(samples):
			devScores[idx1] = list()
			distanceScore = 0.0
			for idx2, toCompare in enumerate(samples):
				if idx1 != idx2:
					if (idx1, idx2) in precomputed:
						indivScore, indivDev = precomputed[(idx1, idx2)]
					else:
						indivScore, indivDev = dtw.getDTW(cycle, toCompare)
						precomputed[(idx1, idx2)] = (indivScore, indivDev)
						precomputed[(idx2, idx1)] = (indivScore, indivDev)
					distanceScore += indivScore
					devScores[idx1].append(indivDev)
			totalDistances.append((idx1, distanceScore))
		if len(samples) != 0:	
			choiceIdx, totalDistance = min(totalDistances, key=lambda x: x[1])
			self.averageCycle = samples[choiceIdx]
<<<<<<< HEAD
=======
			plt.plot([i for i in range(len(self.averageCycle))], [x[1] for x in self.averageCycle], color='blue')
			plt.show()
>>>>>>> 2fec8fd6d02e252dbf8059ae297881306bf5b6bb
			devAgainstAvg = devScores[choiceIdx]
			self.averageDevAgainstTemplate(devAgainstAvg)
		else:
			self.averageCycle = [(0, 0)]
			self.averageDevAgainstTemplate =[(0,0)]
			self.averageDevScore = 0


	

