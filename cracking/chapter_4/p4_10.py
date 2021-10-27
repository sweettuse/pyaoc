__author__ = 'acushner'

# 4.10 Check Subtree: T1 and T2 are two very large binary trees, with T1 much bigger than T2. Create an
# algorithm to determine if T2 is a subtree of T1.
# A tree T2 is a subtree of T1 if there exists a node n in T1 such that the subtree of n is identical to T2.
# That is, if you cut off the tree at node n, the two trees would be identical.
# Hints:#4, #11, #18, #31, #37
from itertools import chain, zip_longest, repeat

from cracking.chapter_4 import BNode
from cracking.chapter_4.p4_2 import short_tree


def pre_order(n: BNode):
    yield n.v
    if n.left:
        yield from pre_order(n.left)
    else:
        yield n.left

    if n.right:
        yield from pre_order(n.right)
    else:
        yield n.right


def find(it, predicate):
    for v in it:
        if predicate(v):
            break

    return it


def is_subtree(head1: BNode, head2: BNode):
    """return True if head2 tree in head1 by equality"""
    it1 = pre_order(head1)
    it2 = pre_order(head2)
    v2 = next(it2)
    it1 = find(it1, lambda v1: v1 == v2)
    return all(v1 == v2 for v1, v2 in zip(chain(it1, repeat(...)), it2))


def __main():
    n1 = short_tree(list(range(31)))
    n2 = short_tree(list(range(15)))
    print(n1.v, n2.v)
    print(is_subtree(n1, n2))


if __name__ == '__main__':
    __main()
