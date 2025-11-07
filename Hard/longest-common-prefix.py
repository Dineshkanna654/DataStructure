class Solution(object):
    def longestCommonPrefix(self, strs):
        """
        :type strs: List[str]
        :rtype: str
        """
        if not strs:
            return ""
        prefix = strs[0]
        result = ''

        for i in range(len(strs)):
            for s in strs[1:]:
                if s[i] != prefix[i]:
                    return result
            result += prefix[i]
        return result
    
# Example usage:
sol = Solution()
print(sol.longestCommonPrefix(["flower","flow","flight"]))  # Output: "fl
print(sol.longestCommonPrefix(["dog","racecar","car"]))     # Output: ""