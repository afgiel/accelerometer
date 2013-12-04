
import preProcess
import stepDetection
# import matplotlib.pyplot as plt
import numpy
import dtw

class Device:
	"""
	Class that stores all the information to create a
	template.


	Considerations:
	Adding more stats on read in data such as average dt

	"""

	def __init__(self, deviceID, lowDT = 120, highDT = 320, minSamples = 150):
		"""


		"""

		self.ID = deviceID
		self.prevTime = None
		self.highDT = highDT
		self.lowDT = lowDT
		self.currIdx = 0
		self.minSamples = minSamples
		self.rawData = list()
		self.rawData.append(list())
		self.processedData = list()



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
		if self.prevTime != None:
			dt = abs(time - self.prevTime)
			if dt > self.highDT or dt < self.lowDT:
				if len(self.rawData[self.currIdx]) >= self.minSamples:
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
		if len(self.rawData[self.currIdx]) < self.minSamples:
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


	def averageCycles(self):
		totalDistances = list()
		devScores = dict()
		precomputed = dict()
		for idx1, cycle in enumerate(self.cycles):
			devScores[idx1] = list()
			distanceScore = 0.0
			for idx2, toCompare in enumerate(self.cycles):
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
		choiceIdx, totalDistance = min(totalDistances, key=lambda x: x[1])
		self.averageCycle = self.cycles[choiceIdx]
		devAgainstAvg = devScores[choiceIdx]
		averageDevAgainstTemplate(devAgainstAvg)

	def averageDevAgainstTemplate(self, devScores):
		avgDevScore = list()
		allScores = list()
		for devScore in devScores:
			for idx, score in enumerate(devScore):
				if allScores[idx] is None:
					allScores[idx] = list()
				allScores[idx].append(score)
		for indexScore in allScores:
			avgForIndex = numpy.mean(indexScore)
			avgDevScore.append(avgForIndex)
		self.averageDevScore = avgDevScore

		

