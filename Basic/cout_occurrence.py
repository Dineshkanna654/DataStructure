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
