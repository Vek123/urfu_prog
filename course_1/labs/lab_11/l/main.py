class Solution:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        if len(s3) != len(s1) + len(s2):
            return False
        elif not s3:
            return True

        dp = [[False] * (len(s2) + 1) for _ in range(len(s1) + 1)]
        dp[0][0] = True
        if s2:
            dp[0][1] = s3[0] == s2[0]
        if s1:
            dp[1][0] = s3[0] == s1[0]
        # i - s1, j - s2
        for i in range(1, len(s1) + 1):
            good = dp[i-1][0] and s1[i-1] == s3[i-1]
            if not good:
                break

            dp[i][0] = good

        for j in range(1, len(s2) + 1):
            good = dp[0][j-1] and s2[j-1] == s3[j-1]
            if not good:
                break

            dp[0][j] = good

        for i in range(1, len(s1) + 1):
            for j in range(1, len(s2) + 1):
                if dp[i-1][j] and s1[i-1] == s3[i+j-1]:
                    dp[i][j] = True
                    continue

                if dp[i][j-1] and s2[j-1] == s3[i+j-1]:
                    dp[i][j] = True

        return dp[-1][-1]
