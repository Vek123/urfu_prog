class Solution:
    decode_map = {str(i - ord("A")+1): chr(i) for i in range(ord("A"), ord("Z")+1)}
    def numDecodings(self, s: str) -> int:
        dp = [0 for _ in range(len(s)+1)]
        dp[0] = 1
        dp[1] = 1 if s[0] in self.decode_map else 0
        for i in range(1, len(s)):
            if s[i] in self.decode_map:
                dp[i+1] += dp[i]
            if s[i-1:i+1] in self.decode_map:
                dp[i+1] += dp[i-1]

        return dp[-1]
