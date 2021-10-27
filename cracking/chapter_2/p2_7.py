__author__ = 'acushner'

# 2.7 Intersection: Given two (singly) linked lists, determine if the two lists intersect. Return the intersecting node. Note that the intersection is defined based on reference, not value. That is, if the kth
# node of the first linked list is the exact same node (by reference) as the jth node of the second
# linked list, then they are intersecting.
# Hints:#20, #45, #55, #65, #76, #93, #111, #120, #129
from cracking.chapter_2 import Node


def intersect(head1: Node, head2: Node):
    for n1 in head1:
        for n2 in head2:
            if n1 is n2:
                return True
    return False


def _get_starting_nodes(head1, head2):
    l1, l2 = len(head1), len(head2)
    if l1 < l2:
        head1, head2 = head2, head1
        l1, l2 = l2, l1

    cur = head1
    for _ in range(l1 - l2):
        cur = cur.next

    cur.display()
    head2.display()
    return cur, head2


def intersect2(head1: Node, head2: Node):
    head1, head2 = _get_starting_nodes(head1, head2)
    for n1, n2 in zip(head1, head2):
        if n1 is n2:
            return n1
    return False


def _get_len_tail(n):
    count = 1
    while n.next:
        n = n.next
        count += 1
    return count, n


def intersect3(head1, head2):
    len1, t1 = _get_len_tail(head1)
    len2, t2 = _get_len_tail(head2)
    if t1 is not t2:
        return False
    first, second = head1, head2
    if len1 < len2:
        first, second = second, first
    for _ in range(abs(len1 - len2)):
        first = first.next

    while True:
        if first is second:
            return first
        first = first.next
        second = second.next



def __main():
    head1 = Node.from_iter('ABCDEF')
    head2 = Node.from_iter('SNTHOEUXYZ')
    head2.next.next.next.next = head1.next.next.next
    head1.display()
    head2.display()
    print(intersect3(head1, head2))
    pass


if __name__ == '__main__':
    __main()
