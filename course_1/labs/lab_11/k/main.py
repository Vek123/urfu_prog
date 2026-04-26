class Solution:
    def findClosest(self, x: int, y: int, z: int) -> int:
        x_z = abs(z - x)
        y_z = abs(z - y)
        if x_z < y_z:
            return 1
        elif x_z > y_z:
            return 2

        return 0
