# Input: "the rain in Spain falls mainly in the plain"
# Output: {'the': 2, 'rain': 1, 'in': 2, 'spain': 1, 'falls': 1, 'mainly': 1, 'plain': 1}

def wordCount(text: str):
	lower_text = text.lower()
	print(lower_text)
	word_list = lower_text.split()
	print(word_list)
	seen = {}
	for word in word_list:
		if (word in seen):
			seen[word] = seen[word] + 1
		else:
			seen[word] = 1
	return seen

print(wordCount('The rain in Spain falls mainly in the plain'))
