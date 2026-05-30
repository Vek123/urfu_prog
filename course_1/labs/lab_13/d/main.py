class Solution:
    def countDigitOccurrences(self, nums: list[int], digit: int) -> int:
        res = 0
        s_digit = str(digit)
        for num in nums:
            res += str(num).count(s_digit)

        return res
