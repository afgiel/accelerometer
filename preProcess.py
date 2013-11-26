
import math

I_TIME = 0
I_X = 1
I_Y = 2
I_Z = 3
I_ID = 4


def resultantAcceleration(T, X, Y, Z):
	return T, math.sqrt(X**2 + Y**2 + Z**2)



#a = a_0 + (t_1 - t_0)*((a_1 - a_0)/(t_1 - t_0))
def linearInterpolation(interval, dataList):
	toReturn = list()
	first = dataList.pop(0)
	firstTime = first[I_TIME]
	first = list(first)
	first[I_TIME] = 0
	toReturn.append(tuple(first))
	prev = first
	lastAddedT = first[I_TIME]
	for T, X in dataList:
		T = T - firstTime
		diff = T - lastAddedT
		numToAdd = diff//interval
		for i in xrange(int(numToAdd)):
			newT = lastAddedT + interval
			TminusT0 = newT - prev[I_TIME]
			T1minusT0 = T - prev[I_TIME]
			X1minusX0 = X - prev[I_X]
			newX = prev[I_X] + TminusT0*(X1minusX0/T1minusT0)
			toAdd = (newT, newX)
			toReturn.append(toAdd)
			lastAddedT = newT
	return toReturn




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
			total += dataList[currentIndex - window + i][1]*(i+1)
			total += dataList[currentIndex + window - i][1]*(i+1)
		total += dataList[currentIndex][1] * (window + 1)
		dataList[currentIndex] =  (dataList[currentIndex][0],(total / numPoints))
		currentIndex += 1

