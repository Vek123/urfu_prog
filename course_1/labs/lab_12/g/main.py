from typing import List


class Solution:
    def canReach(self, arr: List[int], start: int) -> bool:
        curr = [start]
        already = {start}
        while curr:
            new_curr = []
            for i in curr:
                if arr[i] == 0:
                    return True

                if (right := i + arr[i]) < len(arr) and right not in already:
                    new_curr.append(i + arr[i])
                    already.add(right)

                if (left := i - arr[i]) >= 0 and left not in already:
                    new_curr.append(i - arr[i])
                    already.add(left)

            curr = new_curr

        return False
