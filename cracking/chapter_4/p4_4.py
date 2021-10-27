__author__ = 'acushner'

from contextlib import suppress
from functools import lru_cache

from cracking.chapter_4 import BNode
from cracking.chapter_4.p4_2 import short_tree


# 4.4 Check Balanced: Implement a function to check if a binary tree is balanced. For the purposes of
# this question, a balanced tree is defined to be a tree such that the heights of the two subtrees of any
# node never differ by more than one.
# Hints:#27, #33, #49, #705, #724

def is_balanced(n: BNode):
    with suppress(ValueError):
        _height(n)
        return True
    return False


def _height(n: BNode):
    if not n:
        return 0
    h_left, h_right = _height(n.left), _height(n.right)
    if abs(h_left - h_right) > 1:
        raise ValueError(f'unbalanced at {n}')
    return 1 + max(h_left, h_right)


def __main():
    n = short_tree(list(range(12)))
    end = BNode(20, BNode(21), BNode(22))
    # n.left.left.left.left = end
    print(is_balanced(n))
    print(_height.cache_info())
    pass


if __name__ == '__main__':
    __main()
