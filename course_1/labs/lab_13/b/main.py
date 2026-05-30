from typing import List


class Solution:
    def maxIncreaseKeepingSkyline(self, grid: List[List[int]]) -> int:
        res = 0
        rows_max = {}
        cols_max = {}
        for i, row in enumerate(grid):
            for j, col in enumerate(row):
                if i not in rows_max:
                    rows_max[i] = max(row)

                if j not in cols_max:
                    cols_max[j] = max(grid[k][j] for k in range(len(grid)))

                if col == rows_max[i] or col == cols_max[j]:
                    continue

                res += min(rows_max[i] - col, cols_max[j] - col)

        return res
