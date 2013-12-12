for q in 50 100 200
do
	echo "------------- $q Questions ---------------" >> ../data/stats2
	echo >> ../data/stats2
	echo "Threshold Percent 1.03" >> ../data/stats2
	python main.py testFromHalf --numQuestions $q --threshold 1.03 --justTotal >> ../data/stats2
	echo >> ../data/stats2
done