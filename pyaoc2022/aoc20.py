from __future__ import annotations
from dataclasses import dataclass
from operator import attrgetter
from typing import Optional

from pyaoc2019.utils import exhaust, localtimer, read_file, mapt, timer


@dataclass
class Node:
    val: int
    prev: Node = None
    next: Node = None

    def __str__(self):
        return str(self.val)
        # return f'Node({self.val})'

    __repr__ = __str__


class DLL:
    def __init__(self, nums: tuple[int, ...], decryption_key=1):
        self.nodes = self._init_nodes(nums, decryption_key)

    @staticmethod
    def _init_nodes(nums, decryption_key) -> list[Node]:
        nodes = [Node(n * decryption_key) for n in nums]
        cur, *rest = nodes
        cur.next = cur.prev = cur
        head = cur

        for n in rest:
            n.prev = cur
            cur.next = n
            cur = n
        head.prev = cur
        cur.next = head
        return nodes

    def __len__(self):
        return len(self.nodes)

    def __iter__(self):
        cur = self.nodes[0]
        for _ in range(len(self)):
            yield cur
            cur = cur.next

    def move(self, n: Node, amount: int):
        if not amount:
            return

        l = len(self) - 1

        if amount < 0:
            getter = attrgetter('prev')
            amount = abs(amount) % l + 1
        else:
            getter = attrgetter('next')
            amount %= l

        if not amount:
            return

        cur = getter(n)
        self._excise(n)

        for _ in range(amount - 1):
            cur = getter(cur)

        self._insert_right(cur, n)

    def _excise(self, n: Node):
        prev, next = n.prev, n.next
        prev.next, next.prev = next, prev
        n.prev = n.next = None

    def _insert_right(self, right_of: Node, n: Node):
        prev, next = right_of, right_of.next
        prev.next = next.prev = n
        n.prev, n.next = prev, next

    def mix(self):
        for n in self.nodes:
            if debug:
                print('==============')
                print(list(self))
            self.move(n, n.val)
            if debug:
                print(list(self))
                print('==============')

    def find_offset(self, n: Node, amount: int) -> Node:
        res = n
        for _ in range(amount):
            res = res.next
        return res

    def find(self, value: int) -> Node:
        for n in self:
            if n.val == value:
                return n


@timer
def parts1and2(nums, decryption_key=1):
    ll = DLL(nums, decryption_key)
    repeats = 1 if decryption_key == 1 else 10
    for _ in range(repeats):
        ll.mix()
    cur = ll.find(0)
    # print(list(ll))

    res = 0
    for _ in range(3):
        cur = ll.find_offset(cur, 1000)
        res += cur.val
    return res


debug = False
fname = '20.test' if debug else 20

nums = mapt(int, read_file(fname))
print(parts1and2(nums))
print(parts1and2(nums, decryption_key=811589153))
