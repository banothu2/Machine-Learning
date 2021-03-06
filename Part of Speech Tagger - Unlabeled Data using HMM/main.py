'''
	Implementing Part of Speech (POS) tagger from unlabeled data using an HMM

	Tasks: 
		1. Implement Forward-Backward algorithm for a bigram HMM tagger. 
		2. Train this tagger on unlabeled data (data.unlabeled.txt) and report a series of tags for the data. 
			Will use lexicon (data.lexicon.txt) in this step
		3. Tag the unlabeled data (data.unlabeled.txt) with your trained tagger. 
			Write another program that compares the output with the gold standard for data (data.gold.txt) to compute overall accuracy

'''
from mpmath import *

def extract_words_from_file(filename):
	words = set()

	with open(filename) as f:
		data = f.readlines()
	length_of_data = len(data) 

	# REMOVE THIS LINE 
	#length_of_data = 300
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
	#num_of_sentences = 30
	num_of_sentences = len(data)


	# Initialize Counters 
	emissionCounts 		= [[0 for s in range(num_of_words)] for s in range(num_of_tags)]
	transitionCounts 	= [[0 for s in range(num_of_tags)] for s in range(num_of_tags)]
	initialCounts 		= [0]*num_of_tags
	tagCounts 			= [0]*num_of_tags
	
	
	
	for u in range(1):
		# Iterate over each sentence - sentences[s] gives you the sentence
		for s in range(num_of_sentences):
			print s
			# get number of words in sentence 
			words_in_s = data[s].split(' ')
			num_words_in_s = len(words_in_s)
			# Compute forward and backward matrices
			Forward = [[0 for s in range(num_words_in_s)] for s in range(num_of_tags)]
			Backward = [[0 for s in range(num_words_in_s)] for s in range(num_of_tags)]

			# ---- Forward Algorithm 
			# Initialization (first column of trellis)
			c = [0]*num_words_in_s

			c[0] = 0
			for i in range(num_of_tags):
				Forward[i][0] = pi[i]*emission[i][words_lookup[words_in_s[0]]]
				c[0] = c[0] + Forward[i][0]

			# Scale Forward[i][0]
			for i in range(num_of_tags):
				Forward[i][0] = c[0]*Forward[i][0]

			# Intermediate Step 

			for t in range(1, num_words_in_s):
				c[t] = 0
				for i in range(num_of_tags):
					Forward[i][t] = 0
					for j in range(num_of_tags):
						Forward[i][t] = Forward[i][t] + Forward[j][t-1]*transition[j][i]
					Forward[i][t] = Forward[i][t]*emission[i][words_lookup[words_in_s[t]]]
					c[t] = c[t] + Forward[i][t]
				# Scale Forward[i][t]
				if( c[t] != 0):
					c[t] = 1.0 / c[t]
					for i in range(num_of_tags):
						Forward[i][t] = c[t]*Forward[i][t]
				#if(c[t] == 0):
				#	c[t] = 0
				#else:
				#c[t] = 1.0/c[t]
				#for i in range(num_of_tags):
				#	Forward[i][t] = c[t]*Forward[i][t]
		
			# ---- Backward Algorithm 
			# Initialization (first column of trellis)
			for j in range(num_of_tags):
				Backward[j][num_words_in_s - 1] = c[t]


			for t in range(num_words_in_s - 2, -1, -1):
				for i in range(num_of_tags):
					Backward[i][t] = 0
					#sum_over_k = 0
					for j in range(num_of_tags):
						Backward[i][t] = Backward[i][t] + transition[i][j]*emission[j][words_lookup[words_in_s[t+1]]]*Backward[j][t+1]
					# Scale Backward[i][t] with c_t
					Backward[i][t] = Backward[i][t]*c[t]


			
			# prob_of_word = 0
			# for x in range(num_of_tags):
			# 	prob_of_word = prob_of_word + Forward[x][1]*Backward[x][1]

			# print "Probability of word " , prob_of_word


			# prob_of_word = 0
			# for x in range(num_of_tags):
			# 	prob_of_word = prob_of_word + Forward[x][2]*Backward[x][2]
			# print "Probability of word " , prob_of_word
			

			# ----------- SHOULD BE RIGHT UP UNTIL HERE

			# Compute Gamma_3D and Gamma_2D
			# LAST INDEX is NUM WORDS IN S 
			gamma_3D = [[[0 for s in range(num_words_in_s)] for s in range(num_of_tags)] for s in range(num_of_tags)]
			# LAST INDEX IS T
			gamma_2D = [[0 for s in range(num_words_in_s)] for s in range(num_of_tags)]

			for t in range(1, num_words_in_s-1):
				denom = 0
				for i in range(num_of_tags):
					for j in range(num_of_tags):
						denom = denom + Forward[i][t]*transition[i][j]*emission[j][words_lookup[words_in_s[t+1]]]*Backward[j][t+1]

				for i in range(num_of_tags):
					gamma_2D[i][t] = 0
					for j in range(num_of_tags):
						if(denom == 0):
							gamma_3D[i][j][t] = 0
						else: 
							gamma_3D[i][j][t] = (Forward[i][t]*transition[i][j]*emission[j][words_lookup[words_in_s[t+1]]]*Backward[j][t+1])/denom
						gamma_2D[i][t] = gamma_2D[i][t] + gamma_3D[i][j][t]

			# Reestimate A, B, and pi

			# re-estimate pi
			for i in range(num_of_tags):
				pi[i] = gamma_2D[i][0]

			# re-estimate Transition - A
			for i in range(num_of_tags):
				for j in range(num_of_tags):
					numer = 0
					denom = 0
					for t in range(num_words_in_s):
						numer = numer + gamma_3D[i][j][t]
						denom = denom + gamma_2D[i][t]
					if(denom != 0):
						transition[i][j] = numer/denom
					#if(denom == 0):
					#	transition[i][j] = 0
					#else:
					#transition[i][j] = numer/denom

			#re-estimate Emission - B
			for i in range(num_of_tags):
				for j in range(num_of_words):
					numer = 0
					denom = 0
					for t in range(num_words_in_s-1):
						if( words_lookup[words_in_s[t]] == j ):
							numer = numer + gamma_2D[i][t]
						denom = denom + gamma_2D[i][t]
					if(denom != 0):
						emission[i][j] = numer/denom
					#if(denom == 0):
					#	emission[i][j] = 0
					#else:
					#emission[i][j] = numer/denom

			#printMatrix(emission)
			# Compute sum of rows for emission 

			# Compute log[P(O | lambda)]
			#logProb = 0
			#for i in range(words_in_s):
			#	logProb = logProb + log(c[i])
	


	# Viterbi 	
	with open('data/data.gold.txt') as f:
		data = f.readlines()
	len_of_eval_data = len(data) 

	for x in range(10):
		first_sentence = data[x].split(' ')

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
		for x in range(len(words)-2, -1, -1):
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

