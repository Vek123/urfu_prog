class Solution:
    def toHex(self, num: int) -> str:
        if num < 0:
            num = (-num ^ (2**32 - 1)) + 1
        return hex(num)[2:]
