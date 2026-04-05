from threading import Lock
from typing import Callable


class ZeroEvenOdd:
    def __init__(self, n):
        self.n = n
        self.number = 1
        self.locks = [Lock(), Lock(), Lock()]
        self.locks[1].acquire()
        self.locks[2].acquire()
        
        
	# printNumber(x) outputs "x", where x is an integer.
    def zero(self, printNumber: 'Callable[[int], None]') -> None:
        while True:
            self.locks[0].acquire()
            if self.number > self.n:
                self.locks[0].release()
                self.locks[1].release()
                self.locks[2].release()
                break

            printNumber(0)
            self.locks[2 - self.number % 2].release()

    def even(self, printNumber: 'Callable[[int], None]') -> None:
        while True:
            self.locks[2].acquire()
            if self.number > self.n:
                self.locks[2].release()
                break

            printNumber(self.number)
            self.number += 1
            self.locks[0].release()

    def odd(self, printNumber: 'Callable[[int], None]') -> None:
        while True:
            self.locks[1].acquire()
            if self.number > self.n:
                self.locks[1].release()
                break

            printNumber(self.number)
            self.number += 1
            self.locks[0].release()
