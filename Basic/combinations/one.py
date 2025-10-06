# Count total pairs
# Write code to count how many 2-element combinations can be made from a given list.
# Brute force solution
#a = [1, 2, 3]


def main(a):
	pairs = []
	for i in range(len(a)):
		for j in range(i+1, len(a)):
			pairs.append((a[i], a[j]))
	return len(pairs)

# print(main([1, 2, 3, 4]))

def fun2(a):
	n = len(a)
	combination_count = (n * (n - 1)/2)
	return combination_count

#print(fun2([1, 2, 3, 4]))

# Find pairs with difference = 3
# a = [1, 4, 7, 9, 11, 13]

def fun3(a):
    pairs = []
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            if a[j] - a[i] == 3:
                pairs.append((a[i], a[j]))
    return pairs

print(fun3([1, 4, 7, 9, 11, 13]))

