from typing import List


class Solution:
    def getSneakyNumbers(self, nums: List[int]) -> List[int]:
        already = set()
        res = []
        for num in nums:
            if num in already:
                res.append(num)
            else:
                already.add(num)

        return res
