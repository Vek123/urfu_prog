from typing import List


class Solution:
    def binToTime(self, data: list[int]) -> str:
        hours = int("".join(data[:4]), 2)
        minutes = int("".join(data[4:]), 2)
        return f"{hours}:{minutes:02d}"

    def readBinaryWatch(self, turnedOn: int) -> List[str]:
        variants = []
        def dfs(comb: list[str], ones: int, zeros: int) -> None:
            nonlocal variants
            if ones > turnedOn or zeros > (10 - turnedOn):
                return
            if comb[:2] == ["1", "1"]:
                return
            if comb[4:8] == ["1", "1", "1", "1"]:
                return

            if ones + zeros == 10:
                variants.append(comb)
                return

            dfs(comb + ["1"], ones + 1, zeros)
            dfs(comb + ["0"], ones, zeros + 1)

        dfs([], 0, 0)
        return [self.binToTime(data) for data in variants]