__author__ = 'acushner'

# 4.9 BST Sequences: A binary search tree was created by traversing through an array from left to right
# and inserting each element. Given a binary search tree with distinct elements, print all possible
# arrays that could have led to this tree.
# EXAMPLE
# Input:
# Output: {2, 1, 3}, {2, 3, 1}
# Hints: #39, #48, #66, #82
from functools import lru_cache
from itertools import chain, product

from cracking.chapter_4 import BNode
from cracking.chapter_4.p4_2 import short_tree


def possible_inputs(n: BNode):
    @lru_cache(None)
    def _possible_inputs(n):
        if not n:
            return [[]]

        if not (n.left or n.right):
            return [[n.v]]

        l, r = map(possible_inputs, (n.left, n.right))

        res = [[n.v] + vl + vr for vl in l for vr in r]
        res.extend([n.v] + vr + vl for vl in l for vr in r)
        return res
    return _possible_inputs(n)


def __main():
    for size in range(4, 24):
        n = short_tree(list(range(1, size + 1)))
        print(size, len(possible_inputs(n)))
        if size == 11:
            print(possible_inputs(n))


if __name__ == '__main__':
    __main()
