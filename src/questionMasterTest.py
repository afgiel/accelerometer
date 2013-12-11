"""
Code to test functionality of questionMaster.py

"""



import questionMaster

deviceList = [7, 8, 117, 12, 104, 1006, 1000, 1015, 105, 120, 145, 142, 127, 129, 159, 157, 168, 169, 174, 175, 177, 189]
numQuestionsPerDevice = 10
qm = questionMaster.QuestionMaster(deviceList, numQuestionsPerDevice)
for device in deviceList:
	print qm.getQuestions(device)
	qm.answer(device, [1, 0, 1, 0, 0, 0, 0, 0, 0, 0])
	qm.printStatsForDevice(device)
qm.printTotalStats()
