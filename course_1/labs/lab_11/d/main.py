from typing import List


class Solution:
    def minOperations(self, boxes: str) -> List[int]:
        result = []
        for i in range(len(boxes)):
            i_res = 0
            left_acc = 0
            right_acc = 0
            for left in range(0, i):
                if boxes[left] == "1":
                    left_acc += 1
                i_res += left_acc

            for right in range(len(boxes)-1, i, -1):
                if boxes[right] == "1":
                    right_acc += 1
                i_res += right_acc

            result.append(i_res)

        return result
