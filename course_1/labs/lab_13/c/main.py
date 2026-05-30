from collections import deque
from functools import reduce
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def deepestLeavesSum(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0

        que = deque([root])
        while que:
            deepest = True
            leaves = []
            for _ in range(len(que)):
                node = que.popleft()
                if deepest and (node.left or node.right):
                    deepest = False
                else:
                    leaves.append(node)

                if node.left:
                    que.append(node.left)

                if node.right:
                    que.append(node.right)

            if deepest:
                return reduce(lambda acc, curr: acc + curr.val, leaves, 0)

        return 0
