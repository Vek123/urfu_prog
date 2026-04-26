from math import atan, pi
from typing import List


class Solution:
    def find_angle(self, n1: tuple[int, int], n2: tuple[int, int]) -> int:
        xd = abs(n2[1] - n1[1])
        yd = abs(n2[0] - n1[0])
        if xd == 0:
            return 180

        return round(atan(yd/xd)*(180/pi))

    def is_on_one_diag(self, n1: tuple[int, int], n2: tuple[int, int]) -> bool:
        return self.find_angle(n1, n2) == 45

    def solveNQueens(self, n: int) -> List[List[str]]:
        result: list[list[list[str]]] = []
        def dfs(queens: set[tuple[int, int]], start: tuple[int, int], blocked_rows: set[int], blocked_cols: set[int]):
            if len(queens) == n:
                result.append(["".join("Q" if (i, j) in queens else "." for j in range(n)) for i in range(n)])
                return

            for i in range(start[0], n):
                if i in blocked_rows:
                    continue

                for j in range(start[1], n):
                    stop = False

                    if j in blocked_cols:
                        continue
                    for queen in queens:
                        if self.is_on_one_diag((i, j), queen):
                            stop = True
                            break

                    if stop:
                        continue

                    new_queens = queens.copy()
                    new_queens.add((i, j))
                    new_blocked_rows = blocked_rows.copy()
                    new_blocked_cols = blocked_cols.copy()
                    new_blocked_rows.add(i)
                    new_blocked_cols.add(j)
                    dfs(new_queens, (i, 0), new_blocked_rows, new_blocked_cols)

        dfs(set(), (0, 0), set(), set())
        return result
