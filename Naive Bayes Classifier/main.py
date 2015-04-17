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
        }.get(x, -20)  
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
        }.get(x, -30)  
def martial_status(x):
    return {
        'Married-civ-spouse': 0,
        'Divorced': 1,
        'Never-married': 2,
        'Separated': 3,
        'Widowed': 4,
        'Married-spouse-absent': 5,
        'Married-AF-spouse': 6,
        }.get(x, -40) 
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
        'Armed-Forces': 13,
        }.get(x, -50)  
def relationship(x):
    return {
        'Wife': 0,
        'Own-child': 1,
        'Husband': 2,
        'Not-in-family': 3,
        'Other-relative': 4,
        'Unmarried': 5,
        }.get(x, -60) 
def race(x):
    return {
        'White': 0,
        'Asian-Pac-Islander': 1,
        'Amer-Indian-Eskimo': 2,
        'Other': 3,
        'Black': 4,
        }.get(x, -70) 
def sex(x):
    return {
        'Female': 0,
        'Male': 1,
        }.get(x, -80) 
def native_country(x):
    return {
        'United-States': 0,
        'Cambodia': 1,
        'England': 2,
        'Puerto-Rico': 3,
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
        }.get(x, -90) 
def label(x):
	return {
        '>50K\r\n': 0,
        '>50K': 0,
        '<=50K\r\n': 1,
        '<=50K': 1,
        }.get(x, -100) 

def length(x): 
	return {
        0: 8,	# Workclass
        1: 16,	# Education
        2: 7,	# Martial Status
        3: 14,  # Occupation
        4: 6, 	# Relationship
        5: 5,	# Race 
        6: 2,	# Sex
        7: 41,  # Native_country
        8: 2, 	# Label
        }.get(x, -110) 

def parseLine(line):
	l = line.split(',')
	return [
			workclass(l[0]),  
			education(l[1]), 
			martial_status(l[2]), 
			occupation(l[3]), 
			relationship(l[4]), 
			race(l[5]), 
			sex(l[6]), 
			native_country(l[7]), 
			label(l[8])
		]

def get_data_from_file(filename):
	# Open file and read data
	with open(filename) as f:
		data = f.readlines()
	length_of_data = len(data) 

	# Convert data into matrix form using value loop up functions - parseLine
	firstRow = parseLine(data[0])
	matrix = numpy.array(firstRow)
	for x in range(1, length_of_data):
		newRow = parseLine(data[x])
		matrix = numpy.vstack([matrix, newRow])
	return matrix

def seperateDataByLabels(data):
	length_of_data = len(data)
	seperatedByLabels = {}
	for x in range(length_of_data):
		row = data[x]
		label = row[-1]
		if(label not in seperatedByLabels):
			# haven't encountered this class yet - add it to the dictionary
			seperatedByLabels[label] = []
		seperatedByLabels[label].append(row)
	return seperatedByLabels

def generate_maximum_likelihood_estimates(seperatedByLabels):
	MLE_classes = {}
	for i in range(2):
		_class = {}
		num_elements_in_class = len(seperatedByLabels[i])
		for j in range(8):
			_attribute = {}
			for k in range(length(j)):
				count = 0
				for z in range(num_elements_in_class):
					if seperatedByLabels[i][z][j] == k:
						count = count + 1
				_attribute[k] = (count + 1.0) / (num_elements_in_class + length(j))

			_class[j] = _attribute
		MLE_classes[i] = _class
	return MLE_classes

def test_accuracies(test_translated, MLE_classes, seperatedByLabels, training_translated):
	predicted_correctly = []
	for c in range( len(MLE_classes) ):
		predicted_correctly.append(0)

	for x in range(len(test_translated)):
		probabilities = {}
		for i in range( len(MLE_classes) ):
			probability = 1.0
			for j in range(len(test_translated[x])-1):
				probability = probability * MLE_classes[i][j][test_translated[x][j]]
			probability = probability * ((1.0*len(seperatedByLabels[i])) / (1.0*len(training_translated)))
			probabilities[i] = probability
		
		label = 0
		for i in range( len(MLE_classes) ):
			if(probabilities[i] > probabilities[label]):
				label = i

		if (label == test_translated[x][-1]):
			predicted_correctly[label] = predicted_correctly[label] + 1

	num_predicted_correctly = 0
	for c in range( len(MLE_classes) ):
		num_predicted_correctly = num_predicted_correctly + predicted_correctly[c]

	return ((num_predicted_correctly*1.0) / len(test_translated))

# This function doesnt really work for any case lawls - dont use directly!
def find_prob_of_two_factors(attrib, value, attrib_given, value_given, training_seperated_by_labels):
	count = 0.0
	total = len(training_seperated_by_labels[0]) + len(training_seperated_by_labels[1])
	for x in range( len(training_seperated_by_labels[0]) ):
		if(training_seperated_by_labels[0][x][1] == value):
			count = count + 1.0
	#print "Count ", count, " total- ", total
	return count / (total*1.0)

def main():
	# Parse the training data and create a matrix
	training_data = get_data_from_file('q4_data/train_data.txt')
	
	# Seperate data into its individual labels
	training_seperated_by_labels = seperateDataByLabels(training_data)

	# Generate the Maximum Likelihood Estimates - Namely P(X_i = x_ij | Y = y_k) 
	MLE_classes = generate_maximum_likelihood_estimates(training_seperated_by_labels)

	# Parse the test data and create a matrix
	test_translated = get_data_from_file('q4_data/test_data.txt')

	# Seperate data into its individual labels
	test_seperated_by_labels = seperateDataByLabels(test_translated)

	prob_of_50K_or_less_training = (1.0*len(training_seperated_by_labels[1])) / (1.0*len(training_data))
	print "Prior Probability of the label '<=50K' for training data", prob_of_50K_or_less_training

	prob_of_50K_or_less_test = (1.0*len(test_seperated_by_labels[1])) / (1.0*len(training_data))
	print "Prior Probability of the label '<=50K' for testing data", prob_of_50K_or_less_test

	# P(education = 'Bachelors' | label = '>50k') implies P(1 = education('Bachelors') | label = 0)
	prob_edu_and_label = find_prob_of_two_factors(1, 0, 8, 0, training_seperated_by_labels)
	prob_label_greater_than_50k = 1 - prob_of_50K_or_less_training
	#print "prob label greater than 50k ", prob_label_greater_than_50k
	prob_edu_given_label = prob_edu_and_label / prob_label_greater_than_50k
	print "Probability - P(education = 'Bachelors' | label = '>50k')", prob_edu_given_label
	
	# Print out the accuracy of the Naive classifier 
	print test_accuracies(test_translated, MLE_classes, training_seperated_by_labels, training_data)
	

if __name__ == "__main__":
    main()




