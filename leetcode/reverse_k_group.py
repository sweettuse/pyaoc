__author__ = 'acushner'

from typing import Optional


# https://leetcode.com/problems/reverse-nodes-in-k-group/

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __iter__(self):
        cur = self
        while cur:
            yield cur
            cur = cur.next

    def __str__(self):
        return f'Node({self.val})'


class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        return reverse_k_group(head, k)


def _reverse(head, tail):
    """given a head and the final node in that segment, reverse it"""
    if not head:
        return

    cur = head
    prev = None
    while True:
        nxt = cur.next
        cur.next = prev
        if cur is tail:
            break
        prev = cur
        cur = nxt


def _skip(n, k):
    for _ in range(k - 1):
        if n:
            n = n.next
        else:
            return

    return n


def reverse_k_group(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    """iteratively"""
    if k == 1:
        return head

    res = cur = head
    pairs = []
    while True:
        tail = _skip(cur, k)
        pairs.append((cur, tail))
        if not tail:
            break
        cur = tail.next

    prev_head = res
    while pairs:
        head, tail = pairs.pop()

        if tail:
            _reverse(head, tail)
            head, tail = tail, head
            tail.next = prev_head
        prev_head = head
    return prev_head


def reverse_k_group2(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    """recursively"""
    if k == 1:
        return head

    def _rkg(head=head):
        tail = _skip(head, k)
        if not tail:
            return head

        next_head = _rkg(tail.next)
        _reverse(head, tail)
        head, tail = tail, head
        tail.next = next_head
        return head

    return _rkg()


def __main():
    tail = ListNode(5)
    three = ListNode(3, ListNode(4, tail))
    head = ListNode(1, ListNode(2, three))
    for n in head:
        print(n.val)

    # _reverse(head, three)

    reversed = reverse_k_group2(head, 2)
    print('==============')
    for n in reversed:
        print(n)

    pass


if __name__ == '__main__':
    __main()
