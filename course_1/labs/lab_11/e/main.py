# Definition for singly-linked list.

import math
from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def insertGreatestCommonDivisors(self, head: Optional[ListNode]) -> Optional[ListNode]:
        left = head
        while left and left.next:
            gcd = math.gcd(left.val, left.next.val)
            new_node = ListNode(gcd, left.next)
            left.next = new_node
            left = new_node.next

        return head