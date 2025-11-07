# Write a function to find the longest common prefix string amongst an array of strings.

# If there is no common prefix, return an empty string "".

# Example 1:
# Input: strs = ["flower","flow","flight"]
# Output: "fl"

# Example 2:
# Input: strs = ["dog","racecar","car"]
# Output: ""
# Explanation: There is no common prefix among the input strings.

def longestPrefix(strs):
	if not strs:
		return ""

	prefix = strs[0]
	result = ""

	for i in range(len(prefix)):
		for s in strs[1:]:
			if i >= len(s) or prefix[i] != s[i]:
				return result
		result += prefix[i]
	return result


print(longestPrefix(["flower", "flow", "flight"]))
print(longestPrefix(["dog", "racecar", "car"]))
