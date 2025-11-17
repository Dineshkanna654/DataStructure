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

# print(Q1([0, 1, 0, 3, 12]))


# Input: nums = [1,1,2]
# Output: 2, nums = [1,2,_]
# Explanation: Your function should return k = 2, with the first two elements of nums being 1 and 2 respectively.
# It does not matter what you leave beyond the returned k (hence they are underscores).

def Q2(nums):
	k = 0
	for i in range(1, len(nums)):
		if nums[k] != nums[i]:
			k += 1
			nums[k] = nums[i]
	return k +1

print(Q2([1,1,2]))


