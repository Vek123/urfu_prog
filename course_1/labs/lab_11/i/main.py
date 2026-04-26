from typing import List


class Solution:
    def partition(self, s: str) -> List[List[str]]:
        result = []
        def dfs(subs: list[str], curr: str, idx: int):
            for i in range(idx, len(s)):
                sub = curr + s[i]
                if sub == sub[::-1]:
                    subs.append(sub)
                    curr = ""
                    dfs(subs[:-1], sub, i+1)
                else:
                    curr += s[i]

            if not curr:
                result.append(subs)

        dfs([], "", 0)
        return result
