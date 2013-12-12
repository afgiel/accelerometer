
import csv
import collections

with open("../data/sequence_data/1/seq_100197.csv") as train:
	next(train)
	trainReader = csv.reader(train)
	last = None
	diff = collections.Counter()
	current = None
	first = 0
	vlast = 0
	for sample in trainReader:
		if current == None:
			first = current = float(sample[0])
		else:
			last = current
			current = float(sample[0])
			d = abs(current - last)
			diff[d] += 1
	vlast = current
	print vlast - first
			
	print diff.most_common()