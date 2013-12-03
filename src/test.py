import preProcess
import matplotlib.pyplot as plt

MAX_NUM_IDS = 1

TregData = list()
XregData = list()
YregData = list()
ZregData = list()


allData = list()

TnewData = list()
XnewData = list() 
YnewData = list() 
ZnewData = list() 


with open("train.csv") as train:
	next(train)
	numIDs = 0
	prevID = None
	firstTime = None
	for line in train: 
		lineList = [d.strip() for d in line.split(',')]
		lineList = [float(d) for d in lineList]
		T, X, Y, Z, ID = lineList
		if prevID is None or ID != prevID:
			numIDs += 1
			if numIDs > MAX_NUM_IDS: break 
		allData.append(lineList)
		if firstTime is None:
			firstTime = T
			T = 0
		else: 
			T -= firstTime
		TregData.append(T)
		XregData.append(X)
		YregData.append(Y)
		ZregData.append(Z)
		prevID = ID

print "pre-processing"
newData = preProcess.linearInterpolation(1000, allData)
print "done pre-processing"
for new in newData:
	T, X, Y, Z, ID = new
	TnewData.append(T)
	XnewData.append(X)
	YnewData.append(Y)
	ZnewData.append(Z)

print "plotting"
plt.plot(TregData, XregData)
plt.show()
plt.plot(TnewData, XnewData)
plt.show()

plt.plot(TregData, YregData)
plt.show()
plt.plot(TnewData, YnewData)
plt.show()

plt.plot(TregData, ZregData)
plt.show()
plt.plot(TnewData, ZnewData)
plt.show()