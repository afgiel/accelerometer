import numpy as np

def getSlopeForDifference(timeData, diffData):
	X = np.array([[tD, 1] for tD in timeData])
	Y = np.array(diffData)
	line = np.linalg.lstsq(X, Y)[0]
	slope = line[0]
	return slope
