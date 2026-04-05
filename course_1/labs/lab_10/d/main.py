from collections import deque
from typing import Deque, List


class Solution:
    def transformArray(self, nums: List[int]) -> List[int]:
        que: Deque[int] = deque()
        for num in nums:
            if num % 2:
                que.append(1)
            else:
                que.appendleft(0)

        return list(que)
