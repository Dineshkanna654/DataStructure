# Pair students for a project
# You have a list of student names:
students = ["Alice", "Bob", "Charlie", "David", "Eva"]
# ➤ Generate all unique pairs of students to form project teams.

def func(students):
	pairs = []
	for i in range(len(students)):
		for j in range(i+1, len(students)):
			pairs.append((students[i], students[j]))
	return pairs

# print(func(students))

# Find pairs whose average is an integer
# Example: [1, 2, 3, 4, 5, 6]
# ➤ Output: (1,3), (2,4), (3,5), (4,6)

def fun2(a):
	result = []
	all_pairs = []
	for i in range(len(a)):
		for j in range(i+1, len(a)):
			all_pairs.append((a[i], a[j]))
	all_sum = []
	indices_of_integers = []
	for pair in all_pairs:
		sum_of_each_pair = sum(pair)
		all_sum.append(sum_of_each_pair)
	for i, num in enumerate(all_sum):
		if num % 2 == 0:
			indices_of_integers.append(i)
	for index_of_integer in indices_of_integers:
		result.append(all_pairs[index_of_integer])
#	print("all_pairs:", all_pairs)
#	print("all_sum", all_sum)
#	print("indices_of_integers", indices_of_integers)
#	print("result", result)
	# return result

# print(fun2([1, 2, 3, 4, 5, 6]))


# Find the closest pair

# Input: [10, 13, 17, 21, 25]
# ➤ Output: (10, 13) because difference = 3, the smallest.

def fun3(a):
	dics = {}
	diffs = []
	for i in range(len(a)):
		for j in range(i+1, len(a)):
			dics[f"({a[i]}, {a[j]})"] = a[j] - a[i]
	for key, val in dics.items():
		diffs.append(val)
		min_val = min(diffs)
		if val == min_val:
			return key

# print(fun3([10, 13, 17, 21, 25]))

# Generate all unique team matchups

# Input: teams = ["A", "B", "C", "D"]
teams = ["A", "B", "C", "D"]

def fun4(a):
	combs = []
	for i in range(len(a)):
		for j in range(i+1, len(a)):
			combs.append((a[i], a[j]))
	for comb in combs:
		print(comb)

print(fun4(teams))
