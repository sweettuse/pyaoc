from __future__ import annotations

import string
from copy import copy
from typing import List, Iterator, Optional

from cluegen import Datum

__author__ = 'acushner'

from pyaoc2019.utils import exhaust, localtimer

s = '12432111'
s = '1243'
s = '123'

# abc
# lc
# aw

num_char_map = dict(zip(range(1, 27), string.ascii_lowercase))


def decode(s):
    def _helper(ints: Iterator[int]) -> Optional[List[List[int]]]:
        res = [[]]
        try:
            prev = next(ints)
        except StopIteration:
            return res

        for cur in ints:
            comb = 10 * prev + cur
            if comb <= 26:
                for r in _helper(copy(ints)):
                    res.append([*res[0], comb, *r])
            res[0].append(prev)
            prev = cur

        res[0].append(prev)
        return res

    ints = [int(i) for i in s]
    res = _helper(iter(ints))
    print(len(res))
    return {''.join(map(num_char_map.get, r)) for r in res}


class Node(Datum):
    chain: List[int]
    children: Optional[List[Node]] = None

    def __iadd__(self, other: int):
        self.chain.append(other)
        return self

    def pop(self):
        return self.chain.pop()

    def last(self):
        return self.chain[-1]

    def _recurse(self, cur=None):
        cur = (cur or []) + self.chain
        if not self.children:
            yield cur
        else:
            for c in self.children:
                yield from c._recurse(cur)

    def __iter__(self):
        yield from self._recurse()

    def _get_len(self):
        if not self.children:
            yield 1
        else:
            for c in self.children:
                yield from c._get_len()

    def __len__(self):
        return sum(self._get_len())

    @property
    def strings(self):
        return {''.join(map(num_char_map.get, v)) for v in self}


def decode2(s) -> Node:
    """better solution"""
    def _helper(ints: Iterator[int], n: Node):
        for cur in ints:
            prev = n.last()
            if (comb := 10 * prev + cur) <= 26:
                n.pop()
                n.children = [Node([comb]), Node([prev, cur])]
                for child in n.children:
                    _helper(copy(ints), child)
                break
            else:
                n += cur

    it = iter([int(i) for i in s])
    node = Node([next(it)])
    _helper(it, node)
    return node


def __main():
    with localtimer():
        res = decode2('12432111221121211222121122212')
        # res = decode2('1212')
    with localtimer():
        print(len(res))
    with localtimer():
        print(len(res.strings))
        # exhaust(print, sorted(res.strings))


if __name__ == '__main__':
    __main()
