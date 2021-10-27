__author__ = 'acushner'

# 4.6 Successor: Write an algorithm to find the "next" node (i.e., in-order successor) of a given node in a
# binary search tree. You may assume that each node has a link to its parent.
# Hints: #79, #91
from cracking.chapter_4 import BNode
from cracking.chapter_4.p4_2 import short_tree


def lazy_next(n: BNode):
    cur = n
    target = n.v
    while cur.parent:
        cur = cur.parent

    it = iter(cur)
    for n in it:
        if n.v == target:
            break
    return next(it).v


def better(n: BNode):
    if n.right:
        n = n.right
        while n.left:
            n = n.left
        return n.v

    while n.parent and n.parent.right == n:
        n = n.parent

    if not n.parent:
        return

    return n.parent.v


def __main():
    n = short_tree(list(range(15)))
    for t in n:
        print(t)
    pass


if __name__ == '__main__':
    __main()
