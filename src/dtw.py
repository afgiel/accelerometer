import numpy as np

W = 10

def getDTWTuple(A, B):
	a = [x[1] for x in A]
	b = [x[1] for x in B]
	return getDTW(a, b)

# a = [0,0,0,0,1,1,2,2,3,2,1,1,0,0,0,0]
# b = [0,0,1,1,2,2,3,3,3,3,2,2,1,1,0,0]
# dist, dev = getDTW(a, b)
# print dist
# print dev

def getDTW(A, B):
	aLen = len(A)
	bLen = len(B)
	DTW = np.zeros(shape=(aLen, bLen))
	for i in xrange(aLen):
		DTW[i][0] = float('inf')
	for i in xrange(bLen):
		DTW[0][i] = float('inf')
	DTW[0, 0] = 0.

	dev = []

	w = max(W, abs(aLen - bLen))

	lastI = 0
	lastJ = 0

	for i in xrange(1, aLen):
		minCosts = []
		jMin = max(1, i-w)
		jMax = min(bLen, i+w)
		for j in xrange(jMin, jMax):
			cost = abs(A[i] - B[j])
			edits = [(DTW[i-1][j-1], (i-1, j-1))]
			if j != jMin:
				edits.append((DTW[i][j-1], (i, j-1)))
			if j != jMax - 1:
				edits.append((DTW[i-1][j], (i-1, j)))
			minEditCost = min(edits, key=lambda x: x[0])
			DTW[i][j] = cost + minEditCost[0]
			minCosts.append(minEditCost)
		nextInPath = min(minCosts, key=lambda x: x[0])
		newI = nextInPath[1][0]
		newJ = nextInPath[1][1]
		while newI < lastI or newJ < lastJ:
			minCosts.remove(nextInPath)
			nextInPath = min(minCosts, key=lambda x: x[0])
			newI = nextInPath[1][0]
			newJ = nextInPath[1][1]
		dev.append((newI, newJ))
		lastI = newI
		lastJ = newJ

	devToReturn = []
	for index in dev:
		devToReturn.append(DTW[index[0]][index[1]])
		
	return DTW[aLen-1][bLen-1], devToReturn

