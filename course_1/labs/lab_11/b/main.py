from functools import reduce
from itertools import combinations
from typing import List


class Solution:
    def partitions(self, arr: list[int]):
        res = []
        for i in range(1, len(arr)+1):
            res.extend(combinations(arr, i))

        return res

    def bitwise_or(self, vals: List[int]) -> int:
        return reduce(lambda acc, curr: acc | curr, vals, 0)

    def countMaxOrSubsets(self, nums: List[int]) -> int:
        max_val = self.bitwise_or(nums)
        res = 0
        for comb in self.partitions(nums):
            if self.bitwise_or(comb) >= max_val:
                res += 1

        return res