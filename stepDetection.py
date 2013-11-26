

def getAverageCycleLength(dataList, samplesInBaseline = 70, searchArea = 120):
	basePoint = len(dataList)/2
	# Forwards
	diffsF = []
	currPoint = basePoint + samplesInBaseline
	for x in xrange(searchArea):
		diffsF.append((currPoint, sum([abs(dataList[basePoint+n][1] - dataList[currPoint+n][1]) for n in xrange(samplesInBaseline)])))
		currPoint += 1
	# Backwards
	diffsB = []
	currPoint = basePoint - samplesInBaseline
	for x in xrange(searchArea):
		diffsB.append((currPoint, sum([abs(dataList[basePoint+n][1] - dataList[currPoint+n][1]) for n in xrange(samplesInBaseline)])))
		currPoint -= 1

	avgF = min(diffsF, key = lambda x: x[1])[0] - basePoint
	avgB = basePoint - min(diffsB, key = lambda x: x[1])[0]
	return (avgB + avgF)/2.0



def getEstimateOfMin(dataList, cycleLength):
	basePoint = len(dataList)/2
	return 1.2*min([dataList[n][1] for n in xrange(basePoint-int(cycleLength), basePoint+int(cycleLength))])


def getStartIndex(dataList, cycleLength):
	basePoint = len(dataList)/2
	pf = 0
	pb = 0
	maxp = max([(n, dataList[n][1]) for n in xrange(basePoint-int(cycleLength), basePoint+int(cycleLength))], key = lambda x: x[1])[0]
	#Check one
	maxb = max([(n, dataList[n][1]) for n in xrange(maxp-int(.66 *cycleLength), maxp)], key = lambda x: x[1])[0]
	maxf = max([(n, dataList[n][1]) for n in xrange(maxp+3, maxp+int(.66*cycleLength))], key = lambda x: x[1])[0]
	if maxp - maxb < maxf - maxp:
		pb += 1
	else:
		pf +=1
	#Check two
	minb = min([(n, dataList[n][1]) for n in xrange(maxb, maxp)], key = lambda x: x[1])
	minf = min([(n, dataList[n][1]) for n in xrange(maxp, maxf)], key = lambda x: x[1])
	if minb[1] < minf[1]:
		pb += 1
	else:
		pf += 1
	#Check three
	locMaxB = 0
	locMaxF = 0
	prev2 = minb[1]
	prev1 = dataList[minb[0]+1][1]
	curr = dataList[minb[0]+2][1]
	for n in xrange(minb[0]+3, maxp):
		if prev1 > prev2 and prev1 > curr:
			locMaxB+=1
		prev2 = prev1
		prev1 = curr
		curr = dataList[n][1]

	prev2 = dataList[maxp][1]
	prev1 = dataList[maxp+1][1]
	curr = dataList[maxp+2][1]
	for n in xrange(maxp+3, minf[0]):
		if prev1 > prev2 and prev1 > curr:
			locMaxF+=1
		prev2 = prev1
		prev1 = curr
		curr = dataList[n][1]


	if locMaxB < locMaxF:
		pb += 1
	else:
		pf += 1

	#Check four
	db = maxp - minb[0]
	df = minf[0] - maxp

	if db < 10 or df < 10:
		if db <10:
			pf += 1
		if df < 10:
			pb +=1
	else:
		if db < df:
			pb +=1
		else:
			pf +=1

	if pf < pb:
		return minb[0]
	else:
		return minf[0]



def detectAllCycles(cycles, dataList, cycleLength, minVal, si):
	lowBound = 2*int(cycleLength)
	highBound = len(dataList) - 2*int(cycleLength)
	baseidx = si
	nextidx = baseidx + int(cycleLength)
	while nextidx < highBound:
		firstThird = min([(n, dataList[n][1]) for n in xrange(nextidx - int(cycleLength/10.0), nextidx - int(cycleLength/30.0))], key = lambda x: x[1])
		midThird = min([(n, dataList[n][1]) for n in xrange(nextidx - int(cycleLength/30.0), nextidx + int(cycleLength/30.0))], key = lambda x: x[1])
		lastThird = min([(n, dataList[n][1]) for n in xrange(nextidx + int(cycleLength/30.0), nextidx + int(cycleLength/10.0))], key = lambda x: x[1])
		if midThird[1] < firstThird[1]:
			if midThird[1] < lastThird[1]:
				cycles.append([dataList[n] for n in xrange(baseidx, midThird[0]+1)])
				baseidx = midThird[0]
				nextidx = baseidx+ int(cycleLength)
			else:
				prevMin = lastThird
				newMin = lastThird
				while newMin[1] <= prevMin[1]:
					prevMin = newMin
					newMin = min([(n, dataList[n][1]) for n in xrange(prevMin[0]+1, prevMin[0]+1+int(cycleLength/20.0))], key = lambda x: x[1])
				cycles.append([dataList[n] for n in xrange(baseidx, prevMin[0]+1)])
				baseidx = prevMin[0]
				nextidx = baseidx + int(cycleLength)
		else:
			if firstThird[1] < lastThird[1]:
				prevMin = firstThird
				newMin = firstThird
				while newMin[1] <= prevMin[1]:
					prevMin = newMin
					newMin = min([(n, dataList[n][1]) for n in xrange(prevMin[0]-1-int(cycleLength/20.0), prevMin[0]-1)], key = lambda x: x[1])
				cycles.append([dataList[n] for n in xrange(baseidx, prevMin[0]+1)])
				baseidx = prevMin[0]
				nextidx = baseidx + int(cycleLength)
			else:
				prevMin = lastThird
				newMin = lastThird
				while newMin[1] <= prevMin[1]:
					prevMin = newMin
					newMin = min([(n, dataList[n][1]) for n in xrange(prevMin[0]+1, prevMin[0]+1+int(cycleLength/20.0))], key = lambda x: x[1])
				cycles.append([dataList[n] for n in xrange(baseidx, prevMin[0]+1)])
				baseidx = prevMin[0]
				nextidx = baseidx + int(cycleLength)


	baseidx = si
	nextidx = baseidx - int(cycleLength)
	while nextidx > lowBound:
		firstThird = min([(n, dataList[n][1]) for n in xrange(nextidx - int(cycleLength/10.0), nextidx - int(cycleLength/30.0))], key = lambda x: x[1])
		midThird = min([(n, dataList[n][1]) for n in xrange(nextidx - int(cycleLength/30.0), nextidx + int(cycleLength/30.0))], key = lambda x: x[1])
		lastThird = min([(n, dataList[n][1]) for n in xrange(nextidx + int(cycleLength/30.0), nextidx + int(cycleLength/10.0))], key = lambda x: x[1])
		if midThird[1] < firstThird[1]:
			if midThird[1] < lastThird[1]:
				cycles.append([dataList[n] for n in xrange(midThird[0], baseidx+1)])
				baseidx = midThird[0]
				nextidx = baseidx - int(cycleLength)
			else:
				prevMin = lastThird
				newMin = lastThird
				while newMin[1] <= prevMin[1]:
					prevMin = newMin
					newMin = min([(n, dataList[n][1]) for n in xrange(prevMin[0]+1, prevMin[0]+1+int(cycleLength/20.0))], key = lambda x: x[1])
				cycles.append([dataList[n] for n in xrange(prevMin[0], baseidx+1)])
				baseidx = prevMin[0]
				nextidx = baseidx - int(cycleLength)
		else:
			if firstThird[1] < lastThird[1]:
				prevMin = firstThird
				newMin = firstThird
				while newMin[1] <= prevMin[1]:
					prevMin = newMin
					newMin = min([(n, dataList[n][1]) for n in xrange(prevMin[0]-1-int(cycleLength/20.0), prevMin[0]-1)], key = lambda x: x[1])
				cycles.append([dataList[n] for n in xrange(prevMin[0], baseidx+1)])
				baseidx = prevMin[0]
				nextidx = baseidx - int(cycleLength)
			else:
				prevMin = lastThird
				newMin = lastThird
				while newMin[1] <= prevMin[1]:
					prevMin = newMin
					newMin = min([(n, dataList[n][1]) for n in xrange(prevMin[0]+1, prevMin[0]+1+int(cycleLength/20.0))], key = lambda x: x[1])
				cycles.append([dataList[n] for n in xrange(prevMin[0], baseidx+1)])
				baseidx = prevMin[0]
				nextidx = baseidx - int(cycleLength)












