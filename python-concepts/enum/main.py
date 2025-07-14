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

print(q2([10, 15, 20, 25, 30]))
