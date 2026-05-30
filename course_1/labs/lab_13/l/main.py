from typing import List


class Solution:
    def getCommon(self, nums1: List[int], nums2: List[int]) -> int:
        left = set(nums1)
        res = float('inf')
        for i in nums2:
            if i in left:
                res = min(res, i)

        if res == float('inf'):
            res = -1

        return res
