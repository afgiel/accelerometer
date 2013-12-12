import sklearn.metrics as metrics
import matplotlib.pyplot as plt

testResults = {
	1.00: [263, 950, 598, 124],
	1.01: [265, 926, 622, 122],
	1.02: [266, 919, 629, 121],
	1.03: [267, 918, 630, 120],
	1.05: [267, 887, 661, 120],
	1.08: [273, 884, 664, 114],
	1.10: [277, 866, 682, 110],
	1.20: [290, 839, 709, 97],
	1.35: [303, 777, 771, 84],
	1.50: [313, 712, 836, 74]
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
