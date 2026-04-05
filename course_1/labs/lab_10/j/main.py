from threading import Lock
from typing import Callable


class Foo:
    order = [1, 2, 3]
    def __init__(self):
        self.locks = {i: Lock() for i in self.order}
        for lock in self.order[1:]:
            self.locks[lock].acquire()

    def sync_thread(self, thread_id: int, callback: 'Callable[[], None]'):
        next_thread = self.order.index(thread_id) + 1
        self.locks[thread_id].acquire()
        callback()
        self.locks[thread_id].release()
        if next_thread < len(self.order):
            self.locks[self.order[next_thread]].release()

    def first(self, printFirst: 'Callable[[], None]') -> None:
        self.sync_thread(1, printFirst)

    def second(self, printSecond: 'Callable[[], None]') -> None:
        self.sync_thread(2, printSecond)

    def third(self, printThird: 'Callable[[], None]') -> None:
        self.sync_thread(3, printThird)
