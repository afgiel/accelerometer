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
TEST_TEMPLATE_PATH = "../data/test_templates/"


THRESHOLD_PERCENT = 1.05
NUM_QUESTIONS = 2

INITIAL_HIGH_DT = 300
D_HIGH_DT = 25

INITIAL_MIN_TIME = 30000
D_MIN_TIME = 2000

CYCLE_THRESHOLD = 10
D_CYCLE_THRESHOLD = 2



CYCLE_THRESHOLD_IDX = 0
MIN_TIME_IDX = 1
HIGH_DT_IDX = 2
CONSTRAINTS_IT_DICT = {
	1: (CYCLE_THRESHOLD, INITIAL_MIN_TIME - D_MIN_TIME, INITIAL_HIGH_DT),
	2: (CYCLE_THRESHOLD, INITIAL_MIN_TIME - 2*D_MIN_TIME, INITIAL_HIGH_DT),
	3: (CYCLE_THRESHOLD, INITIAL_MIN_TIME - 3*D_MIN_TIME, INITIAL_HIGH_DT),
	4: (CYCLE_THRESHOLD, INITIAL_MIN_TIME - 4*D_MIN_TIME, INITIAL_HIGH_DT),
	5: (CYCLE_THRESHOLD - D_CYCLE_THRESHOLD, INITIAL_MIN_TIME - 5*D_MIN_TIME, INITIAL_HIGH_DT),
	6: (CYCLE_THRESHOLD - D_CYCLE_THRESHOLD, INITIAL_MIN_TIME - 6*D_MIN_TIME, INITIAL_HIGH_DT + D_HIGH_DT),
	7: (CYCLE_THRESHOLD - 2*D_CYCLE_THRESHOLD, INITIAL_MIN_TIME - 7*D_MIN_TIME, INITIAL_HIGH_DT + 2*D_HIGH_DT),
	8: (CYCLE_THRESHOLD - 2*D_CYCLE_THRESHOLD, INITIAL_MIN_TIME - 8*D_MIN_TIME, INITIAL_HIGH_DT + 3*D_HIGH_DT),
	9: (CYCLE_THRESHOLD - 3*D_CYCLE_THRESHOLD, INITIAL_MIN_TIME - 9*D_MIN_TIME, INITIAL_HIGH_DT + 4*D_HIGH_DT),
	10: (CYCLE_THRESHOLD- 3*D_CYCLE_THRESHOLD, INITIAL_MIN_TIME - 10*D_MIN_TIME, INITIAL_HIGH_DT+ 5*D_HIGH_DT),
	11: (CYCLE_THRESHOLD- 4*D_CYCLE_THRESHOLD, INITIAL_MIN_TIME - 11*D_MIN_TIME, INITIAL_HIGH_DT+ 5*D_HIGH_DT),
	12: (CYCLE_THRESHOLD- 4*D_CYCLE_THRESHOLD, INITIAL_MIN_TIME - 11*D_MIN_TIME, INITIAL_HIGH_DT+ 6*D_HIGH_DT),
	13: (CYCLE_THRESHOLD- 4*D_CYCLE_THRESHOLD, INITIAL_MIN_TIME - 11*D_MIN_TIME, INITIAL_HIGH_DT+ 8*D_HIGH_DT),
	14: (CYCLE_THRESHOLD- 4*D_CYCLE_THRESHOLD, INITIAL_MIN_TIME - 11*D_MIN_TIME, INITIAL_HIGH_DT+ 10*D_HIGH_DT),
	15: (CYCLE_THRESHOLD- 4*D_CYCLE_THRESHOLD, INITIAL_MIN_TIME - 11*D_MIN_TIME, INITIAL_HIGH_DT+ 20*D_HIGH_DT),
	16: (CYCLE_THRESHOLD- 4*D_CYCLE_THRESHOLD, INITIAL_MIN_TIME - 11*D_MIN_TIME, INITIAL_HIGH_DT + 30*D_HIGH_DT),
	17: (CYCLE_THRESHOLD- 4*D_CYCLE_THRESHOLD, INITIAL_MIN_TIME - 11*D_MIN_TIME, INITIAL_HIGH_DT + 40*D_HIGH_DT),
	18: (CYCLE_THRESHOLD- 4*D_CYCLE_THRESHOLD, INITIAL_MIN_TIME - 11*D_MIN_TIME, INITIAL_HIGH_DT + 1000*D_HIGH_DT)
}


def extractTemplateForHalf(d, cycleThreshold, verbose = True):
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


def writeTemplateToFile(d, templatePath, verbose = True):
	if verbose:
		print "	Writing template to file for Device", str(d.ID) + "..."
	with open(templatePath + "d_" + str(d.ID) + ".txt", "w") as templateFile:
		toWrite = str([x[1] for x in d.averageCycle])
		templateFile.write(toWrite)					
	if verbose:
		print "	------Template Written------"

def writeDevToFile(d, devPath, verbose =True):
	if verbose:
		print "	Writing develepment score to file for Device", str(d.ID) + "..."
	with open(devPath + "d_" + str(d.ID) + ".txt", "w") as devFile:
		toWrite = str(d.averageDevScore)
		devFile.write(toWrite)
	if verbose:
		print "	------Development Score Written------"
		print


def getTemplateFromFile(path):
	with open(path) as templateFile:
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


def lowerConstraints(iteration, verbose):
	newConstraints = CONSTRAINTS_IT_DICT[iteration]
	if verbose:
		print "		Lowering constraints to:"
		print "			Minimum Time:", newConstraints[MIN_TIME_IDX]
		print "			High Upper bound of dt:", newConstraints[HIGH_DT_IDX]
		print "			Cycle Threshold:", newConstraints[CYCLE_THRESHOLD_IDX]
	return newConstraints

def createAndWriteTemplate(fileNamePath, templatePath, devPath, isTrain, verbose = True):
	cycleThreshold = CYCLE_THRESHOLD
	minTime = INITIAL_MIN_TIME
	highDT = INITIAL_HIGH_DT
	detectedCycles = 0
	currentDevice = None
	iteration = 0
	while (detectedCycles < cycleThreshold):
		if iteration != 0:
			cycleThreshold, minTime, highDT = lowerConstraints(iteration, verbose)
		with open(fileNamePath, "r") as deviceData:
			currentDeviceID = int(next(deviceData))
			deviceReader = csv.reader(deviceData)
			currentDevice = device.Device(currentDeviceID, 0.0, highDT, minTime)
			for sample in deviceReader:
				currentDevice.addSample(float(sample[0]), float(sample[1]), float(sample[2]), float(sample[3]))
		extractTemplateForHalf(currentDevice, cycleThreshold, verbose)
		detectedCycles = len(currentDevice.cycles)
		iteration += 1
					
	writeTemplateToFile(currentDevice, templatePath)
	if isTrain:
		writeDevToFile(currentDevice, devPath)

def getFilePath(deviceID, path):
	return path + "d_" + str(deviceID) + ".txt"

def authenticate(deviceID, questionTemplateFile, thresholdPercent):
	deviceTemplate = getTemplateFromFile(getFilePath(deviceID, DEV_TEMP_FOR_HALF_PATH))
	questionTemplate = getTemplateFromFile(questionTemplateFile)
	avgDevelopmentScore = getTemplateFromFile(getFilePath(deviceID, DEV_DEV_FOR_HALF_PATH))
	dtwScore, seqDev = dtw.getDTW(deviceTemplate, questionTemplate)
	avgDev = getLineForDev(avgDevelopmentScore)
	seqDev = getLineForDev(seqDev)
	avgSlope = linRegress.getSlopeForDifference([i for i in range(len(avgDev))], avgDev)
	seqSlope = linRegress.getSlopeForDifference([i for i in range(len(seqDev))], seqDev)
	return 1 if seqSlope <= avgSlope*thresholdPercent else 0



def trainFromHalf():
	print "Training templates for devices..."
	for fileName in os.listdir(TRAIN_HALF_PATH):
		fileNamePath = os.path.join(TRAIN_HALF_PATH, fileName)
		createAndWriteTemplate(fileNamePath, DEV_TEMP_FOR_HALF_PATH, DEV_DEV_FOR_HALF_PATH, True)



def createTestTemplates():
	print "Creating templates of test data..."
	for fileName in os.listdir(TEST_HALF_PATH):
		fileNamePath = os.path.join(TEST_HALF_PATH, fileName)
		createAndWriteTemplate(fileNamePath, TEST_TEMPLATE_PATH, None, False)
	print "Test template creation complete!"

def testFromHalf(notCreated, thresholdPercent, numQuestions, justTotal):
	if notCreated:
		createTestTemplates()


	# print "Now questioning..."
	qm = questionMaster.QuestionMaster(DEVICES_LIST, numQuestions)
	for deviceID in DEVICES_LIST:
		answers = list()
		questions = qm.getQuestions(deviceID)
		for questionTemplateFile in questions:
			answers.append(authenticate(deviceID, questionTemplateFile, thresholdPercent))
		qm.answer(deviceID, answers)
		if not justTotal:
			qm.printStatsForDevice(deviceID)
	qm.printTotalStats()





