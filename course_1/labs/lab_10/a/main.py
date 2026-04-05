from typing import List


class Solution:
    def alternatingSum(self, nums: List[int]) -> int:
        res = 0
        for idx, num in enumerate(nums):
            if idx % 2:
                res -= num
            else:
                res += num

        return res
