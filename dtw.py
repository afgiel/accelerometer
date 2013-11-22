import numpy as np

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

	for i in xrange(1, aLen):
		minCosts = []
		for j in xrange(1, bLen):
			cost = abs(A[i] - B[j])
			minEditCost = min([DTW[i-1][j], DTW[i][j-1], DTW[i-1][j-1]])
			DTW[i][j] = cost + minEditCost
			minCosts.append(minEditCost)
		dev.append(min(minCosts))

	return DTW[aLen-1][bLen-1], dev

# a = [0,0,0,0,1,1,2,2,3,2,1,1,0,0,0,0]
# b = [0,0,1,1,2,2,3,3,3,3,2,2,1,1,0,0]
# dist, dev = getDTW(a, b)
# print dist
# print dev
