
import preProcess
import stepDetection
import matplotlib.pyplot as plt

class Device:
	"""
	Class that stores all the information to create a
	template.

	Note: avgTime should be passed in as float

	Considerations:
	Adding more stats on read in data such as average dt


	Edge case: last cycle sequence smaller than minSamples
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
		for seq in self.processedData:
			cl = stepDetection.getAverageCycleLength(seq)
			minVal = stepDetection.getEstimateOfMin(seq, cl)
			si = stepDetection.getStartIndex(seq, cl)
			stepDetection.detectAllCycles(self.cycles, seq, cl, minVal, si)


	def averageCycles(self):
		return


		


