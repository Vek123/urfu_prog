from typing import Any, Optional


class Solution:
    def partition(self, head: Optional[Any], x: int) -> Optional[Any]:
        if not head:
            return head

        left = head
        right_side = []
        left_side = []
        while left:
            if left.val < x:
                left_side.append(left)
            else:
                right_side.append(left)

            left = left.next

        for idx, left in enumerate(left_side[:-1]):
            left.next = left_side[idx+1]

        for idx, right in enumerate(right_side[:-1]):
            right.next = right_side[idx+1]

        if left_side and right_side:
            left_side[-1].next = right_side[0]
            right_side[-1].next = None
            head = left_side[0]
        elif left_side:
            left_side[-1].next = None
            head = left_side[0]
        else:
            right_side[-1].next = None
            head = right_side[0]

        return head
