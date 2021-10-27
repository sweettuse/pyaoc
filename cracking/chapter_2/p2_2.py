__author__ = 'acushner'

# 2.2 Return Kth to Last: Implement an algorithm to find the kth to last element of a singly linked list.
# Hints:#8, #25, #41, #67, #126
from typing import Optional

from cracking.chapter_2 import Node


def _find_kth(head: Node, k: int):
    if not head:
        return

    if k <= 0:
        return

    for n, count in zip(head, range(k)):
        pass

    if count != k - 1:
        return

    return n


def kth_to_last(head: Node, k) -> Node:
    kth = _find_kth(head, k)
    if not kth:
        return

    for n, end in zip(head, kth):
        pass

    return n


def kth_to_last_direct(head: Node, k: int) -> Optional[Node]:
    kth = head
    for _ in range(k):
        if not kth:
            return
        kth = kth.next

    for kth_from, end in zip(head, kth):
        pass

    return kth_from


def __main():
    n = Node.from_iter('ABCDEFGHIJKL')
    kth_to_last(n, 11).display()
    pass


if __name__ == '__main__':
    __main()
