__author__ = 'acushner'

# 3.3 Stack of Plates: Imagine a (literal) stack of plates. If the stack gets too high, it might topple.
# Therefore, in real life, we would likely start a new stack when the previous stack exceeds some
# threshold. Implement a data structure SetOfStacks that mimics this. SetO-fStacks should be
# composed of several stacks and should create a new stack once the previous one exceeds capacity.
# SetOfStacks. push() and SetOfStacks. pop() should behave identically to a single stack
# (that is, pop () should return the same values as it would if there were just a single stack).
# FOLLOW UP
# Implement a function popAt ( int index) which performs a pop operation on a specific sub-stack.
# Hints:#64, #87
from cracking.chapter_3 import Stack


class StackWithLen(Stack):
    def __init__(self):
        super().__init__()
        self._size = 0

    def push(self, val):
        super().push(val)
        self._size += 1

    def pop(self):
        self._size -= 1
        return super().pop()

    def __len__(self):
        return self._size


class StackChain:
    def __init__(self, max_size=2):
        self._max_size = max_size
        self._stack_chain = [StackWithLen()]

    def push(self, val):
        if not self._stack_chain or len(self._stack_chain[-1]) >= self._max_size:
            self._stack_chain.append(StackWithLen())
        self._stack_chain[-1].push(val)

    def pop(self, idx=-1):
        if not self._stack_chain[idx]:
            offset = 1
            if idx == -1:
                offset = 0
                self._stack_chain.pop()
            return self.pop(idx - offset)
        return self._stack_chain[idx].pop()

    def peek(self):
        if not self._stack_chain[-1]:
            self._stack_chain.pop()
            return self.peek()
        return self._stack_chain[-1].peek()

    pop_at = pop


def __main():
    sc = StackChain()
    sc.peek()
    for v in range(10):
        sc.push(v)
    # print(sc._stack_chain)
    # for _ in range(2987):
    #     print(sc.pop(), len(sc._stack_chain))

    print(sc.pop(1))
    print(sc.pop(1))
    for _ in range(8):
        print(sc.pop(), len(sc._stack_chain))

    pass


if __name__ == '__main__':
    __main()
