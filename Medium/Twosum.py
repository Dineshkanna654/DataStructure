nums = [2, 7, 11, 15]
target = 9

# for i in range(len(nums)):
#     for j in range(i+1, len(nums)):
#         if nums[i] + nums[j] == target:
#             print(f"Pair found: {nums[i]} and {nums[j]}")

def two_sum(nums, target):
    """
    Given array of integers and target, return indices of two numbers that add up to target.
    
    Time: O(n), Space: O(n)
    """
    seen = {}  # value -> index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            print(seen)
            return [seen[complement], i]
        seen[num] = i
    return []

# Test
print("Two Sum:", two_sum([2, 7, 11, 15], 9))  # [0, 1]