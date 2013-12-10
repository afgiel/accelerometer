import csv
import device
import matplotlib.pyplot as plt

deviceList = list()
with open("../data/raw/train.csv") as trainData:
		next(trainData)
		trainReader = csv.reader(trainData)
		lastIDRead = -1
		deviceIndex = -1
		exceedNumDevicesFlag = False
		for sample in trainReader:
			currentDevice = int(sample[4])
			if currentDevice != lastIDRead:
				if (len(deviceList)+ 1 > 1):
					exceedNumDevicesFlag = True
					break
				deviceIndex += 1
				deviceList.append(device.Device(currentDevice))
				lastIDRead = currentDevice
			deviceList[deviceIndex].addSample(float(sample[0]), float(sample[1]), float(sample[2]), float(sample[3]))

for d in deviceList: 
	raw = d.rawData[len(d.rawData)/2]
	d.preProcessData()
	processed = d.processedData[len(d.processedData)/2]
	print "RAW \n\n\n\n\n"
	print raw
	print "PROCESSED \n\n\n\n"
	print processed
	print len(raw)
	print len(processed)
	print len(deviceList)
	rawStart = raw[0][0]
	plt.plot([x[0] - rawStart for x in raw], [x[1] for x in raw])
	plt.plot([x[0] for x in processed], [x[1] for x in processed])
	plt.show()

