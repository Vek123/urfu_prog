from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def sumNumbers(self, root: Optional[TreeNode]) -> int:
        result = 0
        def dfs(node: Optional[TreeNode], acc: str) -> None:
            nonlocal result
            if not node:
                return

            acc += str(node.val)
            if not node.left and not node.right:
                result += int(acc)
                return

            dfs(node.left, acc)
            dfs(node.right, acc)
        dfs(root, "")
        return result