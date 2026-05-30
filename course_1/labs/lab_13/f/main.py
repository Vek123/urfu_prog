from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def averageOfSubtree(self, root: TreeNode) -> int:
        res = 0
        def dfs(node: Optional[TreeNode]) -> list[int]:
            nonlocal res
            if not node:
                return []

            left = dfs(node.left)
            right = dfs(node.right)

            left_right = left + right + [node.val]
            if sum(left_right) // len(left_right) == node.val:
                res += 1

            return left_right

        dfs(root)
        return res
