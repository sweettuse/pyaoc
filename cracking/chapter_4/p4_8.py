__author__ = 'acushner'

# 4.8 First Common Ancestor: Design an algorithm and write code to find the first common ancestor
# of two nodes in a binary tree. Avoid storing additional nodes in a data structure. NOTE: This is not
# necessarily a binary search tree.
# Hints: #10, #16, #28, #36, #46, #70, #80, #96
from functools import lru_cache

from cracking.chapter_4 import BNode
from cracking.chapter_4.p4_2 import short_tree
from pyaoc2019.utils import timer, localtimer


def find_common(head: BNode, val1, val2):
    vals = {val1, val2}

    def dfs(n):
        def _dfs(n):
            if n.left:
                yield from dfs(n.left)
            yield n.v
            if n.right:
                yield from dfs(n.right)

        return set(_dfs(n))

    def _find_common(n: BNode):
        if not n:
            return False

        left = dfs(n.left)
        right = dfs(n.right)
        print(n.v, left, right, left | right)

        if vals <= left:
            return _find_common(n.left)
        elif vals <= right:
            return _find_common(n.right)
        elif vals <= left | right | {n.v}:
            return n

        return False

    return _find_common(head)


@timer
def find_common2(head: BNode, val1, val2):
    @lru_cache(None)
    def _is_in(n: BNode, val: int):
        if not n:
            return False
        if n.v == val:
            return True
        return _is_in(n.left, val) or _is_in(n.right, val)

    def _find_common(n: BNode):
        if not n:
            return n
        if _is_in(n.left, val1) and _is_in(n.left, val2):
            return _find_common(n.left)

        if _is_in(n.right, val1) and _is_in(n.right, val2):
            return _find_common(n.right)

        return n

    try:
        return _find_common(BNode(None, head))
    finally:
        print(_is_in.cache_info())


def __main():
    max_size = 2 ** 20
    with localtimer():
        n = short_tree(list(range(max_size)))
    print(find_common2(n, 1, max_size - 1))
    pass


if __name__ == '__main__':
    __main()
