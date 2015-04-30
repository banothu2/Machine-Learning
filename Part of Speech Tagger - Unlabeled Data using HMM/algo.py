
# Expectation 
	for each sentence s in S:
		Compute Forward matrix
		Compute Backward matrix

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

# Maximization 
	Pi(t) = initialCounts(t) / (Num of sentences)
	P(t2 | t1) = TransitionCounts(t1, t2) / TagCounts(t1)
	P(w | t) = EmissionCounts(w, t) / TagCounts(t)