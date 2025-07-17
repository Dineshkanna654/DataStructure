# Q1
# Input: 'hello'
# Output:
# 0 h
# 1 e
# 2 l
# 3 l
# 4 o

def q1(text: str):
	for i, char in enumerate(text):
		print(i, char)

#q1('hello')


#Q2. Find the index of all even numbers
# Input: [10, 15, 20, 25, 30]
# Output: Even numbers at indices: [0, 2, 4]

def q2(nums: list):
	output = []
	for i, num in enumerate(nums):
		if (num % 2 == 0):
			output.append(i)
	return output

#print(q2([10, 15, 20, 25, 30]))


#Q3. Convert list of strings to numbered list (starting at 1) 
#Input: ['Learn', 'Code', 'Repeat']
# Output:
# 1. Learn
# 2. Code
# 3. Repeat

def Q3(textList):
	for i, word in enumerate(textList):
		print(f'{i + 1} {word}')

#Q3(['Learn', 'Code', 'Repeat'])


#Q4. Find all indices where the value is greater than 50
# Input: [20, 55, 40, 80, 10, 90]
# Output: Indices with values > 50: [1, 3, 5]

def Q4(nums: list):
	output = []
	for i, num in enumerate(nums):
		if num > 50:
			output.append(i)
	return output


#print(Q4([20, 55, 40, 80, 10, 90]))

#Q5. Replace every third element in a list with 'X'
# Input: ['a', 'b', 'c', 'd', 'e', 'f', 'g']
# Output: ['a', 'b', 'X', 'd', 'e', 'X', 'g']


def Q5(letters: list):
	output = letters.copy()
	for i, word in enumerate(letters):
		if((i+1) % 3 == 0):
			output[i] = "X"
	return output


print(Q5(['a', 'b', 'c', 'd', 'e', 'f', 'g']))




















