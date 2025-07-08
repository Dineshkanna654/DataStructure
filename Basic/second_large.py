#find the second largest number in the list

nums = [1,1,2]

def findTwoMax(nums: list):
	uniq_nums = list(set(nums))
	if (len(uniq_nums) < 2):
		return None
	maxValue = max(uniq_nums)
	uniq_nums.remove(maxValue)
	secondMax = max(uniq_nums)
	return secondMax

print(findTwoMax(nums))
