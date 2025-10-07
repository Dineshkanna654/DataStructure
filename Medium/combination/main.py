# Print unique pairs whose product is even
# Example: [2, 3, 4, 5, 6]
# ➤ Output: (2,3), (2,4), (2,5), (2,6), (3,4), (3,6), (4,5), (4,6), (5,6)

def fun1(a):
	pairs = []
	for i in range(len(a)):
		for j in range(i+1, len(a)):
			if ((a[i] * a[j]) % 2 == 0):
				pairs.append((a[i], a[j]))
	return pairs

# print(fun1([2, 3, 4, 5, 6]))

# Find the pair with the maximum sum
# Input: [1, 5, 7, 9, 2, 8]
# ➤ Output: (9, 8)

def fun2(a):
	all_pairs = []
	all_sum = []
	for i in range(len(a)):
		for j in range(i+1, len(a)):
			all_pairs.append((a[i], a[j]))
	for pair in all_pairs:
		all_sum.append(sum(pair))
	max_sum = max(all_sum)
	max_index = all_sum.index(max_sum)
	max_sum_pair = all_pairs[max_index]
	return max_sum_pair

print(fun2([1, 5, 7, 9, 2, 8]))

# Generate 3-element combinations manually
# Input: [1, 2, 3, 4]
# ➤ Output: (1,2,3), (1,2,4),
