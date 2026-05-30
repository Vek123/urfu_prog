from collections import deque


class Solution:
    def getHappyString(self, n: int, k: int) -> str:
        vals = deque(["a", "b", "c"])
        curr_n = 1
        while curr_n < n:
            for _ in range(len(vals)):
                curr = vals.popleft()
                last = curr[-1]
                if last == "a":
                    vals.append(curr + "b")
                    vals.append(curr + "c")
                elif last == "b":
                    vals.append(curr + "a")
                    vals.append(curr + "c")
                else:
                    vals.append(curr + "a")
                    vals.append(curr + "b")

            curr_n += 1

        if len(vals) < k:
            return ""

        return vals[k-1]
