import sklearn.metrics as metrics
import matplotlib.pyplot as plt

#5 QUESTIONS
# testResults = {
# 	1.00: [263, 950, 598, 124],
# 	1.01: [265, 926, 622, 122],
# 	1.02: [266, 919, 629, 121],
# 	1.03: [267, 918, 630, 120],
# 	1.05: [267, 887, 661, 120],
# 	1.08: [273, 884, 664, 114],
# 	1.10: [277, 866, 682, 110],
# 	1.20: [290, 839, 709, 97],
# 	1.35: [303, 777, 771, 84],
# 	1.50: [313, 712, 836, 74]
# }

#10 QUESTIONS
testResults = {
	1.00: [263, 2095, 1388, 124],
	1.01: [265, 2088, 1395, 122],
	1.02: [266, 2101, 1382, 121],
	1.03: [267, 2133, 1350, 120],
	1.04: [267, 2025, 1458, 120],
	1.05: [267, 2058, 1425, 120],
	1.08: [273, 2006, 1477, 114],
	1.10: [277, 2010, 1473, 110],
	1.20: [290, 1849, 1634, 97],
	1.35: [303, 1756, 1727, 84],
	1.50: [313, 1656, 1827, 74]
}

def calculateAUC(results):
	TP, TN, FP, FN = results
	FPR = float(FP)/(FP + TN)
	TPR = float(TP)/(TP + FN)
	fpr = [0., FPR, 1.]
	tpr = [0., TPR, 1.]
	return metrics.auc(fpr, tpr)

xData = []
yData = []
testKeys = sorted(testResults.keys())
for threshold in testKeys:
	print threshold
	results = testResults[threshold]
	auc = calculateAUC(results)
	print "\t", auc
	xData.append(threshold)
	yData.append(auc)

plt.plot(xData, yData)
plt.show()
