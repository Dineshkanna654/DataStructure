# Input: "the rain in Spain falls mainly in the plain"
# Output: {'the': 2, 'rain': 1, 'in': 2, 'spain': 1, 'falls': 1, 'mainly': 1, 'plain': 1}

def word_count(text: str):
	words_list = text.split()
	output = {}
	for word in words_list:
		output[word] = 2
	return output

# Example usage
text = "the rain in Spain falls mainly in the plain"
result = word_count(text)
print(result)


