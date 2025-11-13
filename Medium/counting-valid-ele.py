# Count how many elements are not equal to a given value.
# nums = [3, 2, 2, 3, 4]
# val = 3

def main(nums, val):
	result = []
	for i in range(len(nums)):
		if nums[i] != val:
			result.append(nums[i])
	return len(result)

print(main([3, 2, 2, 3, 4] , 3))
