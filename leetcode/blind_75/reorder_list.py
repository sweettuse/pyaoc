from itertools import zip_longest, count
from typing import List, Optional


# https://leetcode.com/problems/reorder-list/

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    @classmethod
    def from_list(cls, l: List[int]) -> Optional['ListNode']:
        if not l:
            return
        f, *rest = l
        return cls(f, cls.from_list(rest))

    def __str__(self):
        return str(self.val)

    __repr__ = __str__


def display(n: ListNode):
    print('display', list(traverse(n)))


def traverse(n: ListNode, every=1):
    c = count()
    while n:
        if not next(c) % every:
            yield n
        n = n.next


def interleave(nodes, ends):
    n1, n2 = iter(nodes), iter(ends)
    for t in zip_longest(n1, n2, fillvalue=None):
        for v in t:
            if v is not None:
                yield v
    yield


class Solution:
    def reorderList(self, head: ListNode) -> None:
        """
        Do not return anything, modify head in-place instead.
        """
        nodes = list(traverse(head))
        if not nodes:
            return
        mid = len(nodes) // 2 + 1
        nodes, ends = nodes[:mid], nodes[mid:]

        il = interleave(nodes, reversed(ends))
        cur = next(il)
        for n in il:
            cur.next = n
            cur = n
        display(head)


def _get_mid_end(head):
    found = False
    for mid, end in zip(traverse(head), traverse(head, 2)):
        found = True
    if not found:
        return None, None

    if end.next:
        end = end.next
    assert end.next is None
    return mid, end


def _reverse_2nd_half(mid, end):
    prev, cur = mid, mid.next
    mid.next = None
    while prev is not end:
        next = cur.next
        cur.next = prev
        prev, cur = cur, next
    assert mid.next is None


def _merge(head, end):
    head1, head2 = head, end
    while head2:
        next = head1.next
        head1.next = head2
        head1, head2 = head2, next
    head1.next = None


class Solution2:
    def reorderList(self, head: ListNode) -> None:
        """
        Do not return anything, modify head in-place instead.
        """
        mid, end = _get_mid_end(head)
        _reverse_2nd_half(mid, end)
        _merge(head, end)
        display(head)


if __name__ == '__main__':
    s = Solution2()
    head = ListNode.from_list(range(1, 6))
    s.reorderList(head)
    # print('_____________________')
    head = ListNode.from_list(range(1, 5))
    s.reorderList(head)
