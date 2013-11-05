I_TIME = 0
I_X = 1
I_Y = 2
I_Z = 3
I_ID = 4

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
	for T, X, Y, Z, ID in dataList:
		T = T - firstTime
		diff = T - lastAddedT
		numToAdd = diff//interval
		for i in xrange(int(numToAdd)):
			newT = lastAddedT + interval
			TminusT0 = newT - prev[I_TIME]
			T1minusT0 = T - prev[I_TIME]
			X1minusX0 = X - prev[I_X]
			Y1minusY0 = Y - prev[I_Y]
			Z1minusZ0 = Z - prev[I_Z]
			newX = prev[I_X] + TminusT0*(X1minusX0/T1minusT0)
			newY = prev[I_Y] + TminusT0*(Y1minusY0/T1minusT0)
			newZ = prev[I_Z] + TminusT0*(Z1minusZ0/T1minusT0)
			toAdd = (newT, newX, newY, newZ, ID)
			toReturn.append(toAdd)
			lastAddedT = newT
	return toReturn
