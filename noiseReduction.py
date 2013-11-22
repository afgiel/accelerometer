


# Modifies dataList in place
# a_t = (a_{t-2} + a_{t-1} + a_{t} + a_{t+1} + a_{t+2})/5
def MovingAverage(dataList, window):
	dataSize = len(dataList)
	numPoints = window * 2 + 1
	currentIndex = window
	while(currentIndex + window < dataSize):
		total = 0
		for i in xrange(window):
			total += dataList[currentIndex - window + i]
			total += dataList[currentIndex + window - i]
		total += dataList[currentIndex]
		dataList[currentIndex] = total / numPoints
		currentIndex += 1



# Modifies datalist in place
# a_t = (a_{t-2}*1 + a_{t-1}*2 + a_{t}*3 + a_{t+1}*2 + a_{t+2}*1)/9
def WeightedMovingAverage(dataList, window):
	dataSize = len(dataList)
	numPoints = (window + 1) ** 2
	currentIndex = window
	while(currentIndex + window < dataSize):
		total = 0
		for i in xrange(window):
			total += dataList[currentIndex - window + i]*(i+1)
			total += dataList[currentIndex + window - i]*(i+1)
		total += dataList[currentIndex] * (window + 1)
		dataList[currentIndex] = total / numPoints
		currentIndex += 1

