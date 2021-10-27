__author__ = 'acushner'

# 4.3 List of Depths: Given a binary tree, design an algorithm which creates a linked list of all the nodes
# at each depth (e.g., if you have a tree with depth D, you'll have D linked lists).
# Hints: #107, #123, #135
from typing import List

from cracking.chapter_2 import Node as LinkedList
from cracking.chapter_4 import BNode
from cracking.chapter_4.p4_2 import short_tree


def list_of_depths(n: BNode):
    res = []

    def _list_helper(nodes: list[BNode]):
        if not nodes:
            return
        ll = LinkedList.from_iter(n for n in nodes if n)
        if ll:
            res.append(ll)
            _list_helper([v for n in ll for v in (n.val.left, n.val.right)])

    _list_helper([n])
    return res


def display(nodes: list[LinkedList]):
    max_len = None
    res = []
    while nodes:
        s = nodes.pop().display_str
        if max_len is None:
            max_len = len(s)
        res.append(s.center(max_len))
        # print(max_len, res[-1])

    for s in reversed(res):
        print(s)


def __main():
    t = short_tree(list(range(15)))
    display(list_of_depths(t))


if __name__ == '__main__':
    __main()
