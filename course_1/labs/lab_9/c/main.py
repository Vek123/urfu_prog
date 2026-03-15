from typing import List


class Solution:
    def finalValueAfterOperations(self, operations: List[str]) -> int:
        x = 0
        for operation in operations:
            if operation[0] == "+" or operation[-1] == "+":
                x += 1
            elif operation[0] == "-" or operation[-1] == "-":
                x -= 1

        return x
