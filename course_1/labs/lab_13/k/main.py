from collections import defaultdict
from itertools import chain
from typing import List


class Solution:
    def groupThePeople(self, groupSizes: List[int]) -> List[List[int]]:
        sizes = defaultdict(list)
        for id, size in enumerate(groupSizes):
            if not sizes[size] or len(sizes[size][-1]) == size:
                sizes[size].append([id])
            else:
                sizes[size][-1].append(id)

        return list(chain(*sizes.values()))
