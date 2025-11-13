# Move all zeros to the end of the SAME list, while keeping the order of non-zero elements.
# input [0, 1, 0, 3, 12]
# output [1, 3, 12, 0, 0]

def Q1(nums):
	k = 0
	for i in range(len(nums)):
		if nums[i] != 0:
			nums[k] = nums[i]
			k += 1

	for i in range(k, len(nums)):
		nums[i] = 0
	return nums

print(Q1([0, 1, 0, 3, 12]))


