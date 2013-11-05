import matplotlib.pyplot as plt
import math as m

MAX_NUM_IDS = 1

tData = list()
xData = list()
yData = list()
zData = list()
totalData = list()

with open("train.csv") as train:
	next(train)
	numIDs = 0
	prevID = None
	for line in train: 
		lineList = [d.strip() for d in line.split(',')]
		T, X, Y, Z, ID = lineList[0], lineList[1], lineList[2], lineList[3], lineList[4]
		if prevID is None or ID != prevID:
			numIDs += 1
			if numIDs > MAX_NUM_IDS: break 
		tData.append(T)
		xData.append(X)
		yData.append(Y)
		zData.append(Z)
		total = m.sqrt((pow(float(X), 2) + pow(float(Y), 2) + pow(float(Z), 2)))
		totalData.append(total)
		prevID = ID		

#plt.plot(tData, xData)
#plt.plot(tData, yData)
#plt.plot(tData, zData)
plt.plot(tData, totalData)
plt.show()