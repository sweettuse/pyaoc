__author__ = 'acushner'

from collections import defaultdict
from typing import Any, Callable

from cracking.chapter_3 import Queue


class Graph:
    def __init__(self, nodes: list['Node'] = None):
        self.nodes = nodes or []

    @classmethod
    def from_adj_list(cls, al: list[tuple[Any, Any]], bidir=False):
        res = {}
        for cur, other in al:
            if cur not in res:
                res[cur] = Node(cur)
            if other not in res:
                res[other] = Node(other)
            c, o = res[cur], res[other]
            c.add(o)
            if bidir:
                o.add(c)
        return cls(list(res.values()))


class Node:
    def __init__(self, name):
        self.name = name
        self.children: set[Node] = set()

    def add(self, other: 'Node'):
        self.children.add(other)

    def dfs(self, visited: set['Node'] = None):
        visited = visited if visited is not None else set()
        if self in visited:
            return
        visited.add(self)
        yield self
        for c in self.children:
            yield from c.dfs(visited)

    def bfs(self, visited: set['Node'] = None):
        visited = visited if visited is not None else set()
        q = Queue()
        q.add(self)
        while q:
            cur = q.remove()
            if cur in visited:
                continue
            visited.add(cur)
            yield cur
            for c in cur.children:
                q.add(c)

    def __str__(self):
        return f'Node({self.name})'

    __repr__ = __str__


class BNode:
    """binary node"""

    def __init__(self, v, left=None, right=None):
        self.v = v
        self.left = left
        self.right = right

    def __str__(self):
        return f'BNode({self.v})'

    def __iter__(self):
        if self.left:
            yield from self.left
        yield self
        if self.right:
            yield from self.right

    __repr__ = __str__
