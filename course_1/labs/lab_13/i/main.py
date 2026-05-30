from typing import List


class Solution:
    def numberOfBeams(self, bank: List[str]) -> int:
        res = 0
        prev_ones = 0
        for row in bank:
            ones = 0
            for i in row:
                if i == "1":
                    ones += 1

            if not ones:
                continue

            res += ones * prev_ones
            prev_ones = ones

        return res
