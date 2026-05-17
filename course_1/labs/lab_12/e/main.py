from typing import List


class Solution:
    def solve(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        def dfs(row: int, col: int, component: list[tuple[int, int]], all_vals: set[tuple[int, int]]) -> list[tuple[int, int]] | None:
            if row < 0 or row >= len(board) or col < 0 or col >= len(board[0]):
                return component
            if board[row][col] == 'X':
                return component
            if (row, col) not in all_vals:
                return component

            component.append((row, col))
            all_vals.remove((row, col))
            moves = [
                (row - 1, col),
                (row + 1, col),
                (row, col - 1),
                (row, col + 1),
            ]
            for move in moves:
                dfs(move[0], move[1], component, all_vals)

            return component


        zeros = {(i, j) for i, row in enumerate(board) for j, cell in enumerate(row) if cell == 'O'}
        components = []
        while zeros:
            zero = zeros.pop()
            zeros.add(zero)
            component = dfs(zero[0], zero[1], [], zeros)
            components.append(component)

        for component in components:
            good = False
            for cell in component:
                if cell[0] == 0 or cell[0] == len(board) - 1 or cell[1] == 0 or cell[1] == len(board[0]) - 1:
                    good = True
                    break

            if not good:
                for cell in component:
                    board[cell[0]][cell[1]] = 'X'
