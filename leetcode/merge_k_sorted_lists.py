__author__ = 'acushner'

# Definition for singly-linked list.
from itertools import count
from queue import PriorityQueue
from typing import List, Optional
from heapq import heapify, heappop, heappush


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class ListNodeW:
    def __init__(self, ln):
        self.ln = ln

    def __eq__(self, other):
        return self.ln.val == other.ln.val

    def __lt__(self, other):
        return self.ln.val < other.ln.val


ListNodes = List[Optional[ListNode]]


def get_in_order_orig(nodes: ListNodes):
    nodes = list(map(ListNodeW, nodes))
    heapify(nodes)
    while nodes:
        n = heappop(nodes)
        yield n.ln.val
        if n.ln.next:
            heappush(nodes, ListNodeW(n.ln.next))


def get_in_order(nodes: ListNodes):
    q = PriorityQueue()
    cur = dummy = ListNode(None)
    for n in nodes:
        q.put((n.val, n))
    while q:
        cur.next = q.get()[1]
        cur = cur.next
        if cur.next:
            q.put((cur.next.val, cur.next))
    return dummy.next


class SolutionOrig:
    def mergeKLists(self, lists: ListNodes) -> Optional[ListNode]:
        if not lists:
            return
        nodes = list(filter(bool, lists))
        if not nodes:
            return

        in_order = get_in_order(nodes)
        head = cur = ListNode(next(in_order))
        for v in in_order:
            cur.next = ListNode(v)
            cur = cur.next

        return head


class Solution:
    def mergeKLists(self, nodes: ListNodes) -> Optional[ListNode]:
        c = count()
        q = PriorityQueue()

        def put(n):
            q.put((n.val, next(c), n))

        cur = dummy = ListNode(None)
        for n in nodes:
            put(n)
        while q.qsize():
            cur.next = q.get()[-1]
            cur = cur.next
            if cur.next:
                put(cur.next)
        return dummy.next


def __main():
    pass


if __name__ == '__main__':
    __main()
