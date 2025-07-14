#You are given a list of n numbers taken from the range 0 to n.

def findMiss(nums: list):
	min_num = min(nums)
	max_num = max(nums)
	actual_list = []
	missed_nums = []
	for i in range(min_num, max_num + 1):
		actual_list.append(i)
	for num in actual_list:
		if num not in nums:
			missed_nums.append(num)
	return missed_nums

print(findMiss([3,0,1]))
