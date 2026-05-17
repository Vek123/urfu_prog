class ParkingSystem:

    def __init__(self, big: int, medium: int, small: int):
        self.big_capacity = big
        self.medium_capacity = medium
        self.small_capacity = small
        self.available_spaces = {1: big, 2: medium, 3: small}

    def addCar(self, carType: int) -> bool:
        if self.available_spaces[carType] > 0:
            self.available_spaces[carType] -= 1
            return True

        return False


# Your ParkingSystem object will be instantiated and called as such:
# obj = ParkingSystem(big, medium, small)
# param_1 = obj.addCar(carType)