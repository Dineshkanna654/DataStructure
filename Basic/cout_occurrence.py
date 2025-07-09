"""
Write a function that takes a string and counts the number of occurrences of each letter in the string. The function should return a dictionary with the letters as keys and the counts as values.
Example:
Input: "hello"
Output: {'h': 1, 'e': 1, 'l': 2, 'o': 1}
"""
def count_occurrence(text: str):
    return {letter: text.count(letter) for letter in text}

a = count_occurrence('hello!!')
print(a)

# method 2

def count2(text: str):
	cleaned_text = text.replace(" ", "").lower()
	output = {}
	for letter in cleaned_text:
		if letter.isalpha():
			output[letter] = cleaned_text.count(letter)
	return output

print(count2('Dinesh kanna!'))

# method 3 This avoids using .count() (which scans the string every time).
def count2(text: str):
    output = {}
    for char in text.lower():
        if char.isalpha():
            output[char] = output.get(char, 0) + 1
    return output
