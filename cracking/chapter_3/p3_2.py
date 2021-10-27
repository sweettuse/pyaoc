__author__ = 'acushner'

from cracking.chapter_3 import Stack


# 8.2 Stack Min: How would you design a stack which, in addition to push and pop, has a function min
# which returns the minimum element? Push, pop and min should all operate in 0(1) time.
# Hints:#27, #59, #78

class MinStack(Stack):
    def __init__(self):
        super().__init__()
        self._min = Stack()

    def push(self, val):
        super().push(val)
        if not self._min or val <= self.min:
            self._min.push(val)

    def pop(self):
        v = super().pop()
        if self.min == v:
            self._min.pop()
        return v

    @property
    def min(self):
        return self._min.peek()


def __main():
    stack = MinStack()
    for v in 8, 4, 7, 3, 6, 2:
        stack.push(v)
    while stack:
        print(stack.peek(), stack.min)
        stack.pop()


if __name__ == '__main__':
    __main()
