from collections import Counter


class Solution:
    def longestPalindrome(self, s: str) -> int:
        counts = Counter(s)
        res = 0
        middle = False
        for c in counts.values():
            if c % 2 == 1:
                if not middle:
                    res += 1
                    middle = True

                c -= 1

            if c % 2 == 0:
                res += c

        return res
