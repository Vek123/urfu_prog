from typing import List


class Solution:
    def countPoints(self, points: List[List[int]], queries: List[List[int]]) -> List[int]:
        res = []
        for query in queries:
            curr = 0
            for point in points:
                dst = (abs(point[0] - query[0])**2 + abs(point[1] - query[1])**2)**(1/2)
                if query[2] >= dst:
                    curr += 1

            res.append(curr)

        return res
