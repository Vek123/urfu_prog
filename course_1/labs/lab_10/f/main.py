from functools import reduce


class Solution:
    def numJewelsInStones(self, jewels: str, stones: str) -> int:
        jewels = set(jewels)
        return reduce(lambda acc, curr: (acc + 1) if curr in jewels else acc, stones, 0)
