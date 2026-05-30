from typing import List


class Solution:
    def findThePrefixCommonArray(self, A: List[int], B: List[int]) -> List[int]:
        res = [1 if A[0] == B[0] else 0]
        left, right = {A[0]}, {B[0]}
        for i in range(1, len(A)):
            curr = 0
            if A[i] == B[i]:
                curr += 1
            if A[i] in right:
                curr += 1
            if B[i] in left:
                curr += 1

            right.add(B[i])
            left.add(A[i])
            res.append(res[-1] + curr)

        return res
