
# Helper Functions

def getDifferenceSumPointPair(dataList, samplesInBaseline, currPoint, basePoint):
	diffSum = sum([abs(dataList[basePoint+n][1] - dataList[currPoint+n][1]) for n in xrange(samplesInBaseline)])
	pair = (currPoint, diffSum)
	return pair

def getIndexOfLocalMax(dataList, basePoint, cycleLength):
	return max([(n, dataList[n][1]) for n in xrange(basePoint-int(cycleLength)/2, basePoint+int(cycleLength)/2)], key = lambda x: x[1])[0]







def getAverageCycleLength(dataList, samplesInBaseline = 70, searchArea = 120):
	basePoint = len(dataList)/2
	# Forwards
	diffsF = []
	currPoint = basePoint + samplesInBaseline
	for x in xrange(searchArea):
		diffsF.append(getDifferenceSumPointPair(dataList, samplesInBaseline, currPoint, basePoint))
		currPoint += 1
	# Backwards
	diffsB = []
	currPoint = basePoint - samplesInBaseline
	for x in xrange(searchArea):
		diffsB.append(getDifferenceSumPointPair(dataList, samplesInBaseline, currPoint, basePoint))
		currPoint -= 1
	avgF = min(diffsF, key = lambda x: x[1])[0] - basePoint
	avgB = basePoint - min(diffsB, key = lambda x: x[1])[0]
	return (avgB + avgF)/2.0





def getEstimateOfMin(dataList, cycleLength):
	basePoint = len(dataList)/2
	return 1.2*min([dataList[n][1] for n in xrange(basePoint-int(cycleLength), basePoint+int(cycleLength))])


def getStartIndex(dataList, cycleLength):
	basePoint = len(dataList)/2
	pointsForward = 0
	pointsBackward = 0
	maxPIdx = getIndexOfLocalMax(dataList, basePoint, cycleLength)

	#Check one
	maxbIdx = max([(n, dataList[n][1]) for n in xrange(maxPIdx-int(.66 *cycleLength), maxPIdx-3)], key = lambda x: x[1])[0]
	maxfIdx = max([(n, dataList[n][1]) for n in xrange(maxPIdx+3, maxPIdx+int(.66*cycleLength))], key = lambda x: x[1])[0]
	if maxPIdx - maxbIdx < maxfIdx - maxPIdx:
		pointsBackward += 1
	else:
		pointsForward +=1

	#Check two
	minBackIdxValPair = min([(n, dataList[n][1]) for n in xrange(maxbIdx, maxPIdx)], key = lambda x: x[1])
	minForwIdxValPair = min([(n, dataList[n][1]) for n in xrange(maxPIdx, maxfIdx)], key = lambda x: x[1])
	if minBackIdxValPair[1] < minForwIdxValPair[1]:
		pointsBackward += 1
	else:
		pointsForward += 1

	#Check three
	numLocMaxB = 0
	numLocMaxF = 0
	prev2 = minBackIdxValPair[1]
	prev1 = dataList[minBackIdxValPair[0]+1][1]
	curr = dataList[minBackIdxValPair[0]+2][1]
	for n in xrange(minBackIdxValPair[0]+3, maxPIdx):
		if prev1 > prev2 and prev1 > curr:
			numLocMaxB+=1
		prev2 = prev1
		prev1 = curr
		curr = dataList[n][1]

	prev2 = dataList[maxPIdx][1]
	prev1 = dataList[maxPIdx+1][1]
	curr = dataList[maxPIdx+2][1]
	for n in xrange(maxPIdx+3, minForwIdxValPair[0]):
		if prev1 > prev2 and prev1 > curr:
			numLocMaxF+=1
		prev2 = prev1
		prev1 = curr
		curr = dataList[n][1]

	if numLocMaxB < numLocMaxF:
		pointsBackward += 1
	else:
		pointsForward += 1

	#Check four
	db = maxPIdx - minBackIdxValPair[0]
	df = minForwIdxValPair[0] - maxPIdx

	if db < 10 or df < 10:
		if db < 10:
			pointsForward += 1
		if df < 10:
			pointsBackward +=1
	else:
		if db < df:
			pointsBackward +=1
		else:
			pointsForward +=1

	if pointsForward < pointsBackward:
		return minBackIdxValPair[0]
	else:
		return minForwIdxValPair[0]



def detectAllCycles(cycles, dataList, cycleLength, minVal, startIndex):
	lowBound = 2*int(cycleLength)
	highBound = len(dataList) - 2*int(cycleLength)
	baseidx = startIndex
	nextidx = baseidx + int(cycleLength)
	while nextidx < highBound:
		firstThirdMin = min([(n, dataList[n][1]) for n in xrange(nextidx - int(cycleLength/10.0), nextidx - int(cycleLength/30.0))], key = lambda x: x[1])
		midThirdMin = min([(n, dataList[n][1]) for n in xrange(nextidx - int(cycleLength/30.0), nextidx + int(cycleLength/30.0))], key = lambda x: x[1])
		lastThirdMin = min([(n, dataList[n][1]) for n in xrange(nextidx + int(cycleLength/30.0), nextidx + int(cycleLength/10.0))], key = lambda x: x[1])
		if midThirdMin[1] < firstThirdMin[1]:
			if midThirdMin[1] < lastThirdMin[1]:
				cycles.append([dataList[n] for n in xrange(baseidx, midThirdMin[0]+1)])
				baseidx = midThirdMin[0]
				nextidx = baseidx+ int(cycleLength)
			else:
				prevMin = lastThirdMin
				newMin = lastThirdMin
				nextidx += int(cycleLength/10.0)
				iterations = 0
				while newMin[1] <= prevMin[1] and iterations < 3:
					iterations += 1
					prevMin = newMin
					newMin = min([(n, dataList[n][1]) for n in xrange(nextidx, nextidx + int(cycleLength/20.0))], key = lambda x: x[1])
					nextidx += int(cycleLength/20.0)
				cycle = [dataList[n] for n in xrange(baseidx, prevMin[0]+1)]
				if len(cycle) > cycleLength - 10 and len(cycle) < cycleLength + 10:
					cycles.append(cycle)
				baseidx = prevMin[0]
				nextidx = baseidx + int(cycleLength)
		else:
			if firstThirdMin[1] < lastThirdMin[1]:
				prevMin = firstThirdMin
				newMin = firstThirdMin
				nextidx -= int(cycleLength/10.0)
				iterations = 0
				while newMin[1] <= prevMin[1] and iterations < 3:
					iterations += 1
					prevMin = newMin
					newMin = min([(n, dataList[n][1]) for n in xrange(nextidx-int(cycleLength/20.0), nextidx)], key = lambda x: x[1])
					nextidx -= int(cycleLength/20.0)
				cycle = [dataList[n] for n in xrange(baseidx, prevMin[0]+1)]
				if len(cycle) > cycleLength - 10 and len(cycle) < cycleLength + 10:
					cycles.append(cycle)
				baseidx = prevMin[0]
				nextidx = baseidx + int(cycleLength)
			else:
				prevMin = lastThirdMin
				newMin = lastThirdMin
				nextidx += int(cycleLength/10.0)
				iterations = 0
				while newMin[1] <= prevMin[1] and iterations < 3:
					iterations += 1
					prevMin = newMin
					newMin = min([(n, dataList[n][1]) for n in xrange(nextidx, nextidx + int(cycleLength/20.0))], key = lambda x: x[1])
					nextidx += int(cycleLength/20.0)
				cycle = [dataList[n] for n in xrange(baseidx, prevMin[0]+1)]
				if len(cycle) > cycleLength - 10 and len(cycle) < cycleLength + 10:
					cycles.append(cycle)
				baseidx = prevMin[0]
				nextidx = baseidx + int(cycleLength)


	baseidx = startIndex
	nextidx = baseidx - int(cycleLength)
	while nextidx > lowBound:
		firstThirdMin = min([(n, dataList[n][1]) for n in xrange(nextidx - int(cycleLength/10.0), nextidx - int(cycleLength/30.0))], key = lambda x: x[1])
		midThirdMin = min([(n, dataList[n][1]) for n in xrange(nextidx - int(cycleLength/30.0), nextidx + int(cycleLength/30.0))], key = lambda x: x[1])
		lastThirdMin = min([(n, dataList[n][1]) for n in xrange(nextidx + int(cycleLength/30.0), nextidx + int(cycleLength/10.0))], key = lambda x: x[1])
		if midThirdMin[1] < firstThirdMin[1]:
			if midThirdMin[1] < lastThirdMin[1]:
				cycles.append([dataList[n] for n in xrange(midThirdMin[0], baseidx+1)])
				baseidx = midThirdMin[0]
				nextidx = baseidx - int(cycleLength)
			else:
				prevMin = lastThirdMin
				newMin = lastThirdMin
				nextidx += int(cycleLength/10.0)
				iterations = 0
				while newMin[1] <= prevMin[1] and iterations < 3:
					iterations += 1
					prevMin = newMin
					newMin = min([(n, dataList[n][1]) for n in xrange(nextidx, nextidx + int(cycleLength/20.0))], key = lambda x: x[1])
					nextidx += int(cycleLength/20.0)
				cycle = [dataList[n] for n in xrange(prevMin[0], baseidx+1)]
				if len(cycle) > cycleLength - 10 and len(cycle) < cycleLength + 10:
					cycles.append(cycle)
				baseidx = prevMin[0]
				nextidx = baseidx - int(cycleLength)
		else:
			if firstThirdMin[1] < lastThirdMin[1]:
				prevMin = firstThirdMin
				newMin = firstThirdMin
				nextidx -= int(cycleLength/10.0)
				iterations = 0
				while newMin[1] <= prevMin[1] and iterations < 3:
					iterations += 1
					prevMin = newMin
					newMin = min([(n, dataList[n][1]) for n in xrange(nextidx-int(cycleLength/20.0), nextidx)], key = lambda x: x[1])
					nextidx -= int(cycleLength/20.0)
				cycle = [dataList[n] for n in xrange(prevMin[0], baseidx+1)]
				if len(cycle) > cycleLength - 10 and len(cycle) < cycleLength + 10:
					cycles.append(cycle)
				baseidx = prevMin[0]
				nextidx = baseidx - int(cycleLength)
			else:
				prevMin = lastThirdMin
				newMin = lastThirdMin
				nextidx += int(cycleLength/10.0)
				iterations = 0
				while newMin[1] <= prevMin[1] and iterations < 3:
					iterations += 1
					prevMin = newMin
					newMin = min([(n, dataList[n][1]) for n in xrange(nextidx, nextidx + int(cycleLength/20.0))], key = lambda x: x[1])
					nextidx += int(cycleLength/20.0)
				cycle = [dataList[n] for n in xrange(prevMin[0], baseidx+1)]
				if len(cycle) > cycleLength - 10 and len(cycle) < cycleLength + 10:
					cycles.append(cycle)
				baseidx = prevMin[0]
				nextidx = baseidx - int(cycleLength)












