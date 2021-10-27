__author__ = 'acushner'

from heapq import heapify
from queue import Queue
from random import randint


class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        self.count = 1

    def add(self, val):
        if self.val == val:
            self.count += 1
            return

        if val < self.val:
            self.count += 1
            if self.left:
                self.left.add(val)
            else:
                self.left = Node(val)
        else:
            if self.right:
                self.right.add(val)
            else:
                self.right = Node(val)

    def __str__(self):
        return f'Node({self.val})'

    __repr__ = __str__


def _tree_test():
    vals = [10, 5, 0, 9, 4, 7, 12, -1, 11, 13]
    head = Node(float('inf'))
    for v in vals:
        head.add(v)

    q = Queue()
    cur_lvl = 0
    q.put((head, cur_lvl))
    while q.qsize():
        cur, lvl = q.get()
        if lvl != cur_lvl:
            cur_lvl = lvl
            print()

        print(cur, end=' | ')
        if cur:
            q.put((cur.left, lvl + 1))
            q.put((cur.right, lvl + 1))


def rando_heap(size=14):
    t = [randint(10, 99) for _ in range(size)]
    heapify(t)
    print(t)


def reverse_pairs(nums) -> int:
    nums2 = [2 * n for n in nums]


def __main():
    rando_heap()
    _tree_test()
    pass


if __name__ == '__main__':
    __main()
