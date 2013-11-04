import collections, random


def test(ID, w):
	truePos = 0
	falsePos = 0
	trueNeg = 0
	falseNeg = 0
	total = 0
	for dev in devData.items():
		phi = extractBasicTotalFeatures(dev[1])
		yHat = sparseVectorDotProduct(w, phi)
		if yHat >= 0: 
			if dev[0] == ID:
				truePos += 1
			else: 	
				falsePos += 1
		else: 
			if dev[0] == ID: 
				falsePos += 1
			else: 
				trueNeg += 1
		total += 1
	print "----------------"
	print "Device: %s" % ID
	print "Correct: %f" % (float(truePos + trueNeg)/float(total))
	print "Incorrect: %f" % (float(falsePos + falseNeg)/float(total))
	print "True Positive: %f" % (float(truePos)/float(total))
	print "True Negative: %f" % (float(trueNeg)/float(total))
	print "False Positive: %f" % (float(falsePos)/float(total))
	print "False Negative: %f" % (float(falseNeg)/float(total))
	print "----------------"
	return (float(truePos + trueNeg)/float(total))

def learnWeightsFromPerceptron(ID):
	w = collections.Counter()
	for i in range(ITERS):
		for train in allTrain:
			phi = extractBasicTotalFeatures(train[0])
			yHat = sparseVectorDotProduct(w, phi)
			correct = True
			if yHat >= 0 and train[1] != ID:
				correct = False
			if yHat < 0 and train[1] == ID: 
				correct = False
			if not correct:
				y = 1.0 if yHat < 0 else -1.0
				for feature in phi: 
					w[feature] += y * phi[feature]
	return w				

def extractBasicTotalFeatures(data):
	features = collections.Counter()
	features["X"] = getAvg(data, 1)
	features["Y"] = getAvg(data, 2)
	features["Z"] = getAvg(data, 3)
	return features

def getAvg(data, index):
	total = 0.0
	count = 0.0
	for d in data:
		total += d[index]
		count += 1
	return total/count

def sparseVectorDotProduct(v1, v2):
    if len(v1) > len(v2): v1, v2 = v2, v1
    total = 0
    for i in v1:
        if i in v2: total += v1[i]*v2[i]
    return total

def convertT(T):
	index = T.index("e")
	exp = T[index:]
	num = T[:index]
	exp = int(exp[2:])
	dIndex = num.index(".")
	beforeD = num[:dIndex]
	afterD = num[dIndex+1:]
	numAfterD = len(afterD)
	numZeros = exp - numAfterD
	zeros = ""
	for i in range(numZeros):
		zeros += "0"
	numString = beforeD + afterD + zeros
	return int(numString)

MAX_NUM_IDS = 100
ITERS = 20

initialTimes = dict()
accData = dict()
devData = dict()
weights = dict()
allTrain = set()

print "READING"
with open("train.csv") as train:
	next(train)
	numIDs = 0
	prevID = None
	for line in train: 
		lineList = [d.strip() for d in line.split(',')]
		T, X, Y, Z, ID = lineList[0], lineList[1], lineList[2], lineList[3], lineList[4]
		#if "e" in T: T = convertT(T)
		if prevID is None or ID != prevID:
			numIDs += 1
			if numIDs > MAX_NUM_IDS: break 
			prevID = ID
			initialTimes[ID] = float(T)
			initialData = (0, float(X), float(Y), float(Z))
			accData[ID] = list()
			accData[ID].append(initialData)
		else: 
			newData = (float(T) - initialTimes[ID], float(X), float(Y), float(Z))
			accData[ID].append(newData)
		prevID = ID	

print "SPLITTING"
for indivData in accData.items(): 
	ID = indivData[0]
	length = len(indivData[1])
	setLength = length/4
	training1 = indivData[1][:setLength]
	training2 = indivData[1][setLength+1:2*setLength]
	training3 = indivData[1][(setLength*2)+1:3*setLength]
	dev = indivData[1][(3*setLength)+1:]
	devData[ID] = dev
	allTrain.add((tuple(training1), ID))
	allTrain.add((tuple(training2), ID))
	allTrain.add((tuple(training3), ID))

print "TRAINING"
for training in accData.items():
	ID = training[0]
	weights[ID] = learnWeightsFromPerceptron(ID)

print "TESTING"
totalCorrectPercent = float(0)
for dev in devData.items():
	ID = dev[0]
	w = weights[ID]
	totalCorrectPercent += test(ID, w)

print "Cumulative Correctness: %f" % (totalCorrectPercent/float(MAX_NUM_IDS))





