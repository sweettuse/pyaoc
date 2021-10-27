__author__ = 'acushner'

# 3.5 Sort Stack: Write a program to sort a stack such that the smallest items are on the top. You can use
# an additional temporary stack, but you may not copy the elements into any other data structure
# (such as an array). The stack supports the following operations: push, pop, peek, and is Empty.
# Hints: #15, #32, #43
from random import shuffle

from cracking.chapter_3 import Stack


class SortedStack:
    def __init__(self):
        self._main = Stack()
        self._buffer = Stack()

    @staticmethod
    def _move_from_to(s1, s2):
        while s1:
            s2.push(s1.pop())

    def _to_main(self):
        self._move_from_to(self._buffer, self._main)

    def _to_buffer(self):
        self._move_from_to(self._main, self._buffer)

    def push(self, val):
        """ insert 2
        _main: [7, 5, 3] """
        self._to_buffer()
        while self._buffer:
            cur = self._buffer.pop()
            if val >= cur:
                self._buffer.push(cur)
                self._buffer.push(val)
                break
            self._main.push(cur)
        else:
            self._buffer.push(val)

        self._to_main()

    def pop(self):
        self._to_main()
        return self._main.pop()

    def peek(self):
        self._to_main()
        return self._main.peek()

    def __bool__(self):
        return bool(self._main or self._buffer)


def sort_stack(s: Stack):
    buffer = Stack()
    while s:
        cur = s.pop()
        while buffer and buffer.peek() > cur:
            s.push(buffer.pop())
        buffer.push(cur)
    while buffer:
        s.push(buffer.pop())


def __main():
    s = Stack()
    l = list(range(12))
    shuffle(l)
    for v in l:
        s.push(v)
    print(l)
    sort_stack(s)
    print(s)
    return
    ss = SortedStack()
    ss.push(7)
    ss.push(5)
    # print('jeb', ss._main)
    ss.push(3)
    print('jeb', ss._main)
    print('jeb', ss._main)
    print('jeb', ss._main)
    ss.push(8)
    print('jeb', ss._main)
    while ss:
        print(ss.pop())

    pass


if __name__ == '__main__':
    __main()
