# Definition for a binary tree node.
from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        res = []
        que = deque([root])
        while que:
            curr = []
            for _ in range(len(que)):
                node = que.popleft()
                if not node:
                    continue

                curr.append(node.val)
                que.append(node.left)
                que.append(node.right)

            if curr:
                res.append(curr)

        return res
                