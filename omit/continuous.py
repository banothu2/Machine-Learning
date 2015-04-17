'''
	Implementing Naive Bayes Classifier 

	Related files: 
		readme.txt 			-- This file provides information about the format of the data provided
		train_data.txt 		-- This file contains the training data for the Naive Bayes Classifier
		test_data.txt 		-- This file contains the test data for the Naive Bayes Classifier

	Input: Modified version of the 1994 U.S.A Census Data
	Task: Predict whether the income of the person exceeds $50K/yr based on census data. 



 	git clone git://github.com/numpy/numpy.git numpy
'''
import numpy
import math 

# Global Variables 
features = 9 

def workclass(x):
    return {
        'Private': 0,
        'Self-emp-not-inc': 1,
        'Self-emp-inc': 2,
        'Federal-gov': 3,
        'Local-gov': 4,
        'State-gov': 5,
        'Without-pay': 6,
        'Never-worked': 7,
        }.get(x, -1)  
def education(x):
    return {
        'Bachelors': 0,
        'Some-college': 1,
        '11th': 2,
        'HS-grad': 3,
        'Prof-school': 4,
        'Assoc-acdm': 5,
        'Assoc-voc': 6,
        '9th': 7,
        '7th-8th': 8,
        '12th': 9,
        'Masters': 10,
        '1st-4th': 11, 
        '10th': 12,
        'Doctorate': 13,
        '5th-6th': 14,
        'Preschool': 15,
        }.get(x, -1)  
def martial_status(x):
    return {
        'Married-civ-spouse': 0,
        'Divorced': 1,
        'Never-married': 2,
        'Separated': 3,
        'Widowed': 4,
        'Married-spouse-absent': 5,
        'Married-AF-spouse': 6,
        }.get(x, -1) 
def occupation(x):
    return {
        'Tech-support': 0,
        'Craft-repair': 1,
        'Other-service': 2,
        'Sales': 3,
        'Exec-managerial': 4,
        'Prof-specialty': 5,
        'Handlers-cleaners': 6,
        'Machine-op-inspct': 7,
        'Adm-clerical': 8,
        'Farming-fishing': 9,
        'Transport-moving': 10,
        'Priv-house-serv': 11, 
        'Protective-serv': 12,
        'Armed-Force': 13,
        }.get(x, -1)  
def relationship(x):
    return {
        'Wife': 0,
        'Own-child': 1,
        'Husband': 2,
        'Not-in-family': 3,
        'Other-relative': 4,
        'Unmarried': 5,
        }.get(x, -1) 
def race(x):
    return {
        'White': 0,
        'Asian-Pac-Islander': 1,
        'Amer-Indian-Eskimo': 2,
        'Other': 3,
        'Black': 4,
        }.get(x, -1) 
def sex(x):
    return {
        'Female': 0,
        'Male': 1,
        }.get(x, -1) 
def native_country(x):
    return {
        'United-States': 0,
        'Cambodia': 1,
        'England': 2,
        'Puerto-Ric': 3,
        'Canada': 4,
        'Germany': 5,
        'Outlying-US(Guam-USVI-etc)': 6,
        'India': 7,
        'Japan': 8,
        'Greece': 9,
        'South': 10,
        'China': 11, 
        'Cuba': 12,
        'Iran': 13,
        'Honduras': 14,
        'Philippines': 15,
        'Italy': 16,
        'Poland': 17,
        'Jamaica': 18,
        'Vietnam': 19,
        'Mexico': 20,
        'Portugal': 21,
        'Ireland': 22,
        'France': 23,
        'Dominican-Republic': 24,
        'Laos': 25,
        'Ecuador': 26,
        'Taiwan': 27,
        'Haiti': 28,
        'Columbia': 29,
        'Hungary': 30,
        'Guatemala': 31,
        'Nicaragua': 32,
        'Scotland': 33,
        'Thailand': 34,
        'Yugoslavia': 35,
        'El-Salvador': 36,
        'Trinadad&Tobago': 37,
        'Peru': 38,
        'Hong': 39,
        'Holand-Netherlands': 40,
        }.get(x, -1) 
def label(x):
	return {
        '>50K\r\n': 0,
        '>50K': 0,
        '<=50K\r\n': 1,
        '<=50K': 1,
        }.get(x, -1) 

def parseLine(line):
	l = line.split(',')
	return [workclass(l[0]),  education(l[1]), martial_status(l[2]), occupation(l[3]), relationship(l[4]), race(l[5]), sex(l[6]), native_country(l[7]), label(l[8])]


def main():

	# parse the data 
	with open('q4_data/train_data.txt') as f:
		training_data = f.readlines()
	length_of_training_data = len(training_data) 

	firstRow = parseLine(training_data[0])
	training_translated = numpy.array(firstRow)
	#for x in range(1, length_of_training_data):
	for x in range(1, 10):
		newRow = parseLine(training_data[x])
		training_translated = numpy.vstack([training_translated, newRow])
	#print training_translated
	#print training_translated.transpose()
	#print training_translated.dot(2)

	# training 
		# need mean and standard deviation for each attribute (9) and class value (2)
		# So, we need 18 attribute summaries

	# TASK: TRAINING 
	# for each attribute, calculate the mean and standard deviation 
		# Example: [[1,20,1], [2,21,0], [3,22,1], [4,22,0]]
		# Result:  {0: [(3.0, 1.4142135623730951), (21.5, 0.7071067811865476)], 1: [(2.0, 1.4142135623730951), (21.0, 1.4142135623730951)]}

	# 1. Seperate Data by Class
	# 2. Calculate Mean	
	# 3. Calculate Standard Deviation
	# 4. Summarize Dataset
	# 5. Summarize Attributes by Class
	
	seperatedByLabels = {}
	mean_and_std = {}
	for x in range(0, 10):
		row = training_translated[x]
		label = row[-1]
		if(label not in seperatedByLabels):
			# haven't encountered this class yet - add it to the dictionary
			seperatedByLabels[label] = []
			mean_and_std[label] = []
		seperatedByLabels[label].append(row)

	for x in range(len(mean_and_std)):
		mean_and_std[x] = zip(numpy.mean(seperatedByLabels[x], axis=0), numpy.std(seperatedByLabels[x], axis=0))
	print mean_and_std[0][1]

	# Prediction
	# 1. Calculate Gaussian Probability Density Function
	# 2. Calculate Class Probabilities
	# 3. Make a Prediction
	# 4. Estimate Accuracy

	# Get Test Data 
	with open('q4_data/test_data.txt') as test_data_file:
		test_data = test_data_file.readlines()
	length_of_test_data = len(test_data) 

	firstRowTest = parseLine(test_data[0])
	test_translated = numpy.array(firstRowTest)
	#for x in range(1, length_of_training_data):
	for x in range(1, 10):
		newRow = parseLine(test_data[x])
		test_translated = numpy.vstack([test_translated, newRow])

	# Calculate the probabilities

	calculateClassProbabilities(mean_and_std, test_translated[0])

def calculateClassProbabilities(mean_and_std, test_data):
	prediction_for_each_class = {}
	keys = mean_and_std.keys()
	for i in range(len(keys)):
		if(keys[i] not in prediction_for_each_class):
			prediction_for_each_class[keys[i]] = []

		# For each class label
		class_label = keys[i]
		probabilities = 1
		for j in range(features - 1):
			# For each attribute
			mean = mean_and_std[class_label][j][0]
			std = mean_and_std[class_label][j][1]
			x = test_data[j]
			probability = (1 / (std*math.sqrt(2*math.pi)))*(math.exp(-(math.pow(x - mean, 2))/(2*math.pow(std, 2))))
			probabilities = probabilities * probability

		prediction_for_each_class[class_label].append(probabilities)
	print prediction_for_each_class

if __name__ == "__main__":
    main()




