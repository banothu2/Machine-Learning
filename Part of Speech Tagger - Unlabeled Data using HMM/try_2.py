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
		for z in range(1, len(l)):
			tags.add(l[z])
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
	#length_of_data = 10
	# REMOVE THIS LINE 

	lookup_ctr = 0
	for x in range(length_of_data):
		l = data[x].split(' ')
		for y in range(len(l)):
			if l[y] not in words_lookup:
				words_lookup[l[y]] = lookup_ctr
				lookup_ctr = lookup_ctr + 1


	#words = extract_words_from_file('data/data.unlabeled.txt')
	num_of_words = len(words_lookup)
	uniform_for_words = 1.0/num_of_words
	#print num_of_words


	word_tag_lookup = {}
	tags_lookup = {}
	with open('data/data.lexicon.txt') as f:
		data_tags = f.readlines()
	length_of_data_tags = len(data_tags)

	lookup_ctr_tags = 0
	for x in range(length_of_data_tags):
		l = data_tags[x].split(' ')
		for y in range(1, len(l)):
			if l[y] not in tags_lookup:
				tags_lookup[l[y]] = lookup_ctr_tags
				lookup_ctr_tags = lookup_ctr_tags + 1

		word_tag_lookup[words_lookup[l[0]]] = []
		for y in range(2, len(l)):
			word_tag_lookup[words_lookup[l[0]]] =  word_tag_lookup[words_lookup[l[0]]] + [tags_lookup[l[y]]]

	#print word_tag_lookup

	#print tags_lookup


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
	
	
	for u in range(1):
		# Iterate over each sentence - sentences[s] gives you the sentence
		for s in range(10):
			# get number of words in sentence 
			words_in_s = data[s].split(' ')
			num_words_in_s = len(words_in_s)
			# Compute forward and backward matrices
			Forward = [[0 for s in range(num_words_in_s)] for s in range(num_of_tags)]
			Backward = [[0 for s in range(num_words_in_s)] for s in range(num_of_tags)]

			# ---- Forward Algorithm 
			# Initialization (first column of trellis)
			for j in range(num_of_tags):
				Forward[j][0] = pi[j]*emission[j][words_lookup[words_in_s[0]]]

			# Intermediate Steps - All subsequent columns
			# sum all incoming transition probabilies
			for i in range(1, num_words_in_s):
				for j in range(num_of_tags):
					sum_incoming_transitions = 0
					for k in range(num_of_tags):
						sum_incoming_transitions = sum_incoming_transitions + Forward[k][i-1]*transition[k][j]*emission[j][words_lookup[words_in_s[i]]]
					Forward[j][i] = sum_incoming_transitions

			# Final Steps (last column of trellis)
			#sum_last_column = 0
			#for k in range(num_of_tags):
			#	sum_last_column = sum_last_column + Forward[k][2]
			#print "Chosen Val ", sum_last_column


			# Initialization (first column of trellis)
			for j in range(num_of_tags):
				Backward[j][2] = 1

			# Intermediate Steps - All subsequent columns
			# sum all incoming transition probabilies
			for i in range(num_words_in_s - 2, -1, -1):
				for j in range(num_of_tags):
					sum_over_k = 0
					for k in range(num_of_tags):
						sum_over_k = sum_over_k + transition[j][k]*emission[k][words_lookup[words_in_s[i+1]]]*Backward[k][i+1]
					Backward[j][i] = sum_over_k

			#For every word/tag pair (w, t):
			for w in range(num_words_in_s):
				sum_of_fwd_tags = 0
				for t in range(num_of_tags):
					sum_of_fwd_tags = sum_of_fwd_tags + Forward[t][w]

				for t in range(num_of_tags):
					if(words_in_s[w] in word_tag_lookup):
						if(t in word_tag_lookup[words_in_s[w]]):
							emissionCounts[t][w] = emissionCounts[t][w] + (Forward[t][w]*Backward[w][t])/sum_of_fwd_tags

			for t1 in range(num_of_tags):
				for t2 in range(num_of_tags):
					for w in range(num_of_words-1):
						#TransitionCounts(t1,t2) += forward[t1][i]*P(t2|t1)*P(w[i+1]|t2)*backward[t2][i+1] / (sum of forward[tag][N] for all tags)
						transitionCounts[t2][t1] = transitionCounts[t2][t1] + (Forward[t1][w]*Backward[w+1][t]*transition[t2][t1]*emission[t2][words_lookup[words_in_s[w+1]]])


	'''
		• For each sentence s in S:
			○ For each word/tag pair (w,t):
				§ For every occurence of w (at position i) in s:
					□ EmissionCounts(w,t) += (forward[t][i]*backward[t][i])/(sum of forward[tag][N] for all tags)
			○ For every tag/tag pair:
				§ For every adjacent pair of words (starting at position i):
					□ TransitionCounts(t1,t2) += forward[t1][i]*P(t2|t1)*P(w[i+1]|t2)*backward[t2][i+1] / (sum of forward[tag][N] for all tags)
			○ For every tag:
				§ For the first word in the sentence:
					□ InitialCounts(t) = pi(t)*P(w[1]|t)*backward[t][1] / (sum forward[t][N] for all tags)
		• For each tag t:
			○ For every word w:
				§ TagCounts(t) += EmissionCounts(w,t)
	'''

	# Viterbi 	
	with open('data/data.gold.txt') as f:
		data = f.readlines()
	len_of_eval_data = len(data) 

	first_sentence = data[0].split(' ')

	words = []
	tags = []
	for x in range(len(first_sentence )-1):
		blah = first_sentence[x].split('_')
		words.append(blah[0])
		tags.append(blah[1])
	#print words
	#print tags
	for t in range(len(tags)):
		tags[t] = tags_lookup[tags[t]]
		#print first_sentence[x]



	Viterbi = [[0 for s in range(len(words))] for s in range(num_of_tags)] 
	backpointer = [[0 for s in range(len(words))] for s in range(num_of_tags)]

	for j in range(num_of_tags):
		Viterbi[j][0] = pi[j]*emission[j][words_lookup[words[0]]]
		backpointer[j][0] = -1

	# Intermediate Steps - All subsequent columns
	for i in range(1, len(words)):
		for j in range(num_of_tags):
			k_vals = []
			for k in range(num_of_tags):
				k_vals.append(Viterbi[k][i-1]*transition[k][j])
			#print k_vals
			k_star = max(k_vals)
			k_index = k_vals.index(k_star)
			Viterbi[j][i] = Viterbi[k_index][i-1]*transition[k_index][j]*emission[j][words_lookup[words[i]]]
			if Viterbi[j][i] == 0:
				backpointer[j][i] = -1
			else:
				backpointer[j][i] = k_index


	# Final Steps (last column of trellis)
	k_vals = []
	for k in range(num_of_tags):
		k_vals.append(Viterbi[k][len(words)-1])
	#print k_vals
	k_star = max(k_vals)
	k_index = k_vals.index(k_star)

	array = [0]*len(words)
	array[len(words)-1] = k_index
	for x in range(num_of_tags, -1, -1):
		array[x] = backpointer[array[x+1]][x+1]

	print tags
	print array



	#words_in_test = data[1].split(' ')


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

