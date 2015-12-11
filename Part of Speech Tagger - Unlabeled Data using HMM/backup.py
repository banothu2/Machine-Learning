'''
	Implementing Part of Speech (POS) tagger from unlabeled data using an HMM

	Tasks: 
		1. Implement Forward-Backward algorithm for a bigram HMM tagger. 
		2. Train this tagger on unlabeled data (data.unlabeled.txt) and report a series of tags for the data. 
			Will use lexicon (data.lexicon.txt) in this step
		3. Tag the unlabeled data (data.unlabeled.txt) with your trained tagger. 
			Write another program that compares the output with the gold standard for data (data.gold.txt) to compute overall accuracy

'''

def extract_words_from_file(filename):
	words = set()

	with open(filename) as f:
		data = f.readlines()
	length_of_data = len(data) 

	# REMOVE THIS LINE 
	length_of_data = 10
	# REMOVE THIS LINE 

	for x in range(length_of_data):
		l = data[x].split(' ')
		for y in range(len(l)):
			words.add(l[y])
	return words

def extract_tags_from_file(filename):
	tags = set()

	with open(filename) as f:
		data = f.readlines()
	length_of_data = len(data)

	for x in range(length_of_data):
		l = data[x].split(' ')
		tags.add(l[1])
	return tags

def printMatrix(A):
	print('\n'.join(['   '.join(['{0:.8f}'.format(item) for item in row]) 
      for row in A]))

def main():


	#words = set()
	words_lookup = {}
	with open('data/data.unlabeled.txt') as f:
		data = f.readlines()
	length_of_data = len(data) 

	# REMOVE THIS LINE 
	length_of_data = 10
	# REMOVE THIS LINE 

	lookup_ctr = 0
	for x in range(length_of_data):
		l = data[x].split(' ')
		for y in range(len(l)):
			if l[y] not in words_lookup:
				words_lookup[l[y]] = lookup_ctr
				lookup_ctr = lookup_ctr + 1
			#words.add(l[y])


	#words = extract_words_from_file('data/data.unlabeled.txt')
	num_of_words = len(words_lookup)
	uniform_for_words = 1.0/num_of_words
	print num_of_words

	tags = extract_tags_from_file('data/data.lexicon.txt')
	num_of_tags = len(tags)
	uniform_for_tags = 1.0/num_of_tags

	pi 			= [uniform_for_tags]*num_of_tags
	transition 	= [[0 for s in range(num_of_tags)] for s in range(num_of_tags)]
	emission 	= [[0 for s in range(num_of_words)] for s in range(num_of_tags)]

	
	# Uniform initialization for transition matrix
	for i in range(num_of_tags):
		for j in range(num_of_tags):
			transition[i][j] =  uniform_for_tags
	
	# Uniform initialization for emission matrix 
	for i in range(num_of_tags):
		for j in range(num_of_words):
			emission[i][j] = uniform_for_words
	

	# Implementing 

	# Get each sentence from unlabeled data 
	filename_unlabeled_data = 'data/data.unlabeled.txt'
	with open(filename_unlabeled_data) as f:
		sentences = f.readlines()
	num_of_sentences = 10
	#num_of_sentences = len(data)


	# Initialize Counters 
	emissionCounts 		= [[0 for s in range(num_of_words)] for s in range(num_of_tags)]
	transitionCounts 	= [[0 for s in range(num_of_tags)] for s in range(num_of_tags)]
	initialCounts 		= [0]*num_of_tags
	tagCounts 			= [0]*num_of_tags
	
	# Iterate over each sentence - sentences[s] gives you the sentence
	for s in range(1):
		# get number of words in sentence 
		words_in_s = data[x].split(' ')
		num_words_in_s = len(words_in_s)
		# Compute forward and backward matrices
		Forward = [[0 for s in range(num_words_in_s)] for s in range(num_of_tags)]
		Backward = [[0 for s in range(num_words_in_s)] for s in range(num_of_tags)]

		# ---- Forward Algorithm 
		# Initialization (first column of trellis)
		for j in range(3):
			Forward[j][0] = pi[j]*emission[j][word[0]]

		# Intermediate Steps - All subsequent columns
		# sum all incoming transition probabilies
		for i in range(1, 3):
			for j in range(3):
				sum_incoming_transitions = 0
				for k in range(3):
					print trans[k][j], trans[j][k]
					sum_incoming_transitions = sum_incoming_transitions + Forward[k][i-1]*trans[k][j]*emission[j][word[i]]

				Forward[j][i] = sum_incoming_transitions

		# Final Steps (last column of trellis)
		#sum_last_column = 0
		#for k in range(3):
		#	sum_last_column = sum_last_column + Forward[k][2]
		#print "Chosen Val ", sum_last_column


		# Initialization (first column of trellis)
		for j in range(3):
			Backward[j][2] = 1

		# Intermediate Steps - All subsequent columns
		# sum all incoming transition probabilies
		for i in range(1, -1, -1):
			print i
			for j in range(3):
				sum_over_k = 0
				for k in range(3):
					sum_over_k = sum_over_k + trans[j][k]*emission[k][word[i+1]]*Backward[k][i+1]
				Backward[j][i] = sum_over_k




		'''
		for each word/tag pair (w, t)
			for every occurance of w (at position i) in s:
				emissionCounts(w, t) += (forward[t][i]*backward[t][i]) / (sum of forward[tag][N] for all tags)			-- This can be cached apparently?
			for every tag/tag pair:
				for every adjacent pair of words (starting at position i):
					transitionCounts(t1, t2) += forward[t1][i]*P(t2 | t1)*P(w[i+1] | t2)*backward[t2][i+1] / (sum of forward[tag][N] for all tags)
			for every tag: 
				for the first word in the sentence:
					initialCounts(t) = pi(t)*P(w[1] | t)*backward[t][1] / (sum forward[t][N] for all tags)
		for each tag t: 
			for every word w: 
				tagCounts(t) += emissionCounts(w, t)
		'''


		
		prob_of_word = 0
		for x in range(num_of_tags):
			prob_of_word = prob_of_word + Forward[x][num_words_in_s-1]*Backward[x][num_words_in_s-1]

		print prob_of_word

		prob_of_word = 0
		for x in range(num_of_tags):
			prob_of_word = prob_of_word + Forward[x][num_words_in_s-1]*Backward[x][num_words_in_s-1]

		print prob_of_word

		
	'''
	print "transition matrix "
	print printMatrix(transition)
	'''
	'''
	print "Emission matrix"
	print printMatrix(emission)
	'''
	#words = extract_words_from_file('data/data.unlabeled.txt')
	#tags = extract_tags_from_file('data/data.lexicon.txt')
	#print len(words), len(tags)
	#print len(tags)
	# 17 tags and 7574 unique words 






	return 0


if __name__ == "__main__":
    main()

