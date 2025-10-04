# Print all pairs that sum to 10

a = [1, 2, 3, 7, 8, 9, 5]

for i in range(len(a)):
	for j in range(i+1, len(a)):
		sum = a[i] + a[j]
		if (sum == 10):
			print((a[i], a[j]))
			
# 
