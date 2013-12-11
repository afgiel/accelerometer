import os
import csv
import questionMaster
import device
import dtw
import linRegress

DEVICES_LIST = [7, 8, 9, 12, 23, 25, 26, 27, 33, 37, 39, 45, 47, 51, 52, 57, 58, 
65, 67, 68, 70, 71, 73, 74, 75, 78, 79, 81, 87, 89, 90, 91, 92, 94, 95, 96, 99, 
104, 105, 108, 110, 111, 116, 117, 120, 122, 124, 126, 127, 129, 134, 137, 142, 
145, 148, 149, 152, 156, 157, 158, 159, 162, 163, 168, 169, 174, 175, 177, 183, 
187, 188, 189, 190, 194, 196, 204, 206, 207, 211, 213, 216, 219, 222, 224, 229, 
232, 233, 234, 236, 237, 239, 240, 261, 263, 268, 269, 270, 271, 273, 274, 275, 
277, 281, 282, 283, 284, 285, 289, 290, 291, 294, 296, 297, 298, 299, 302, 306, 
309, 312, 313, 314, 323, 325, 333, 335, 338, 341, 343, 344, 345, 350, 360, 361, 
366, 369, 370, 371, 376, 378, 381, 390, 394, 398, 399, 401, 404, 411, 412, 413, 
415, 417, 421, 422, 423, 425, 433, 438, 447, 448, 455, 461, 463, 466, 471, 473, 
477, 478, 479, 482, 485, 486, 487, 491, 492, 494, 501, 503, 505, 507, 509, 514, 
515, 518, 520, 523, 524, 528, 531, 533, 534, 536, 537, 539, 547, 550, 552, 553, 
554, 556, 557, 562, 568, 571, 573, 574, 575, 577, 579, 580, 581, 583, 589, 593, 
594, 595, 596, 600, 601, 607, 610, 611, 612, 613, 614, 617, 621, 622, 626, 627, 
629, 632, 634, 638, 640, 642, 643, 646, 647, 650, 653, 656, 658, 660, 661, 663, 
664, 665, 666, 667, 669, 670, 671, 674, 675, 676, 678, 679, 680, 681, 682, 683, 
684, 687, 688, 690, 691, 692, 694, 696, 698, 699, 700, 703, 705, 706, 709, 710, 
711, 713, 714, 720, 721, 722, 727, 728, 729, 730, 732, 735, 736, 738, 739, 745, 
746, 750, 751, 754, 755, 757, 761, 762, 763, 764, 768, 770, 774, 776, 781, 782, 
784, 789, 792, 793, 795, 801, 802, 804, 805, 806, 810, 812, 814, 818, 820, 823, 
824, 827, 834, 836, 838, 839, 841, 842, 846, 847, 848, 854, 857, 859, 860, 862, 
864, 868, 870, 871, 877, 880, 882, 883, 887, 890, 895, 897, 900, 911, 912, 913, 
919, 933, 941, 943, 945, 953, 955, 956, 967, 973, 977, 979, 983, 987, 991, 992, 
996, 997, 998, 1000, 1006, 1015, 1017, 1027, 1029, 1031, 1033, 1035, 1036, 1037]

TRAIN_HALF_PATH = "../data/train_data/"
TEST_HALF_PATH = "../data/test_data/"
DEV_TEMP_FOR_HALF_PATH = "../data/device_templates_for_half_data/"
DEV_DEV_FOR_HALF_PATH = "../data/device_dev_for_half_data/"
INITIAL_HIGH_DT = 300
D_HIGH_DT = 100
INITIAL_MIN_TIME = 20000
MIN_TIME_FLOOR = 14001
D_MIN_TIME = 2000
NUM_QUESTIONS = 5
CYCLE_THRESHOLD = 2
THRESHOLD_PERCENT = 1.05


def extractTemplateForHalf(d, cycleThreshold = CYCLE_THRESHOLD, verbose = True):
	if verbose:
		print "	------Reading Complete------"
		print "	Preprocessing data from Device", str(d.ID) + "..."
	d.preProcessData()
	if verbose:
		print "	------Preprocessing Complete------"
		print "	Detecting cycles from Device", str(d.ID) + "..."
	d.detectCycles()			
	if verbose:
		print "	------Cycle Detection Complete------"
	if (len(d.cycles) < cycleThreshold):
		if verbose:
			print "	Only", len(d.cycles), "detected cycles" 
			print "	Restarting average cycle detection with lower constraints"
		return
	if verbose:
		print "	Detected ", len(d.cycles), "cycles"
		print "	Averaging cycles from Device", str(d.ID) + "..."	
	d.averageCycles()
	if verbose:
		print "	------Template Created------"


def writeTempAndDevToFile(d, verbose =True):
	if verbose:
		print "	Writing template to file for Device", str(d.ID) + "..."
	with open(DEV_TEMP_FOR_HALF_PATH + "d_" + str(d.ID) + ".txt", "w") as templateFile:
		toWrite = str([x[1] for x in d.averageCycle])
		templateFile.write(toWrite)					
	if verbose:
		print "	------Templates Written------"
		print "	Writing develepment score to file for Device", str(d.ID) + "..."
	with open(DEV_DEV_FOR_HALF_PATH + "d_" + str(d.ID) + ".txt", "w") as devFile:
		toWrite = str(d.averageDevScore)
		devFile.write(toWrite)
	if verbose:
		print "	------Development Score Written------"
		print


def getTemplateFromFile(ID, path , prefix = "d_"):
	filename = path + prefix + str(ID) + ".txt"
	with open(filename) as templateFile:
		templateStr = next(templateFile)
	templateStr = templateStr[1:len(templateStr)-1]
	template = templateStr.split(',')
	template = [float(x) for x in template]
	return template

def getLineForDev(dev):
	toReturn = list()
	for idx, score in enumerate(dev):
		toReturn.append(score)
		if idx != 0:
			toReturn[idx] += toReturn[idx-1]
	return toReturn



def createAndWriteTemplate(fileNamePath, toWrite = True, cycleThreshold = CYCLE_THRESHOLD):
	minTime = INITIAL_MIN_TIME
	highDT = INITIAL_HIGH_DT
	detectedCycles = 0
	currentDevice = None
	while (detectedCycles < cycleThreshold):
		with open(fileNamePath, "r") as deviceData:
			currentDeviceID = int(next(deviceData))
			deviceReader = csv.reader(deviceData)
			currentDevice = device.Device(currentDeviceID, 0.0, highDT, minTime)
			for sample in deviceReader:
				currentDevice.addSample(float(sample[0]), float(sample[1]), float(sample[2]), float(sample[3]))
			extractTemplateForHalf(currentDevice, cycleThreshold, toWrite)
			minTime -= D_MIN_TIME
			if minTime < MIN_TIME_FLOOR:
				highDT += D_HIGH_DT*10
			detectedCycles = len(currentDevice.cycles)
			if (detectedCycles < cycleThreshold):
				if toWrite:
					print "		Lowering constraints to:"
					print "			Minimum Time:", minTime
					print "			High Upper bound of dt:", highDT
	if toWrite:
		writeTempAndDevToFile(currentDevice)
	return currentDevice.averageCycle

def getQuestionTemplate(questionFile):
	averageCycle = createAndWriteTemplate(questionFile, False)
	return [x[1] for x in averageCycle]

def authenticate(deviceID, questionFile):
	deviceTemplate = getTemplateFromFile(deviceID, DEV_TEMP_FOR_HALF_PATH)
	questionTemplate = getQuestionTemplate(questionFile)
	avgDevelopmentScore = getTemplateFromFile(deviceID, DEV_DEV_FOR_HALF_PATH)
	dtwScore, seqDev = dtw.getDTW(deviceTemplate, questionTemplate)
	avgDev = getLineForDev(avgDevelopmentScore)
	seqDev = getLineForDev(seqDev)
	avgSlope = linRegress.getSlopeForDifference([i for i in range(len(avgDev))], avgDev)
	seqSlope = linRegress.getSlopeForDifference([i for i in range(len(seqDev))], seqDev)
	return 1 if seqSlope <= avgSlope*THRESHOLD_PERCENT else 0



def trainFromHalf():
	for fileName in os.listdir(TRAIN_HALF_PATH):
		fileNamePath = os.path.join(TRAIN_HALF_PATH, fileName)
		createAndWriteTemplate(fileNamePath)



def testFromHalf():
	qm = questionMaster.QuestionMaster(DEVICES_LIST, NUM_QUESTIONS)
	for deviceID in DEVICES_LIST:
		answers = list()
		questions = qm.getQuestions(deviceID)
		for questionFile in questions:
			answers.append(authenticate(deviceID, questionFile))
		qm.answer(deviceID, answers)
		qm.printStatsForDevice(deviceID)
	qm.printTotalStats()





