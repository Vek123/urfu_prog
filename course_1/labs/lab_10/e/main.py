from typing import Any, Optional


class Solution:
    def mergeNodes(self, head: Optional[Any]) -> Optional[Any]:
        left = head
        before = None
        while left:
            if not left.val:
                if not before:
                    if left is head:
                        head = left.next

                    left = left.next
                    continue

                before.next = left.next
                before = left.next
                left = left.next
            else:
                if before:
                    before.val += left.val
                    before.next = left.next
                else:
                    before = left

            if left:
                left = left.next

        return head
