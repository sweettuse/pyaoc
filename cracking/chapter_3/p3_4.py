__author__ = 'acushner'

# 3.4 Queue via Stacks: Implement a MyQueue class which implements a queue using two stacks.
# Hints: #98, #7 74
from cracking.chapter_3 import Stack


class Queue:
    def __init__(self):
        self.back = Stack()
        self.front = Stack()

    @staticmethod
    def _move_from_to(s1: Stack, s2: Stack):
        while s1:
            s2.push(s1.pop())

    def add(self, val):
        self._move_from_to(self.front, self.back)
        self.back.push(val)

    def remove(self):
        self._move_from_to(self.back, self.front)
        return self.front.pop()

    def peek(self):
        self._move_from_to(self.back, self.front)
        return self.front.peek()


def __main():
    q = Queue()
    q.add(1)
    q.add(2)
    q.add(3)
    print(q.remove())
    print(q.remove())
    # print(q.peek())
    q.add(4)
    q.add(5)
    q.add(6)
    print(q.remove())
    print(q.remove())
    print(q.remove())
    print(q.remove())
    print(q.remove())
    print(q.remove())
    print(q.remove())
    print(q.remove())

    pass


if __name__ == '__main__':
    __main()
