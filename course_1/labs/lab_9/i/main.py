class Solution:
    def maxDistinct(self, s: str) -> int:
        exists = set()
        res = 0
        for i in s:
            if i not in exists:
                res += 1
                exists.add(i)

        return res
