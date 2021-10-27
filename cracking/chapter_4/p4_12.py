__author__ = 'acushner'

# 4.12 Paths with Sum: You are given a binary tree in which each node contains an integer value (which
# might be positive or negative). Design an algorithm to count the number of paths that sum to a
# given value. The path does not need to start or end at the root or a leaf, but it must go downwards
# (traveling only from parent nodes to child nodes).
# Hints:#6, #14, #52, #68, #77, #87, #94, #103, #108, #115
from collections import Counter, deque

from cracking.chapter_4 import BNode
from cracking.chapter_4.p4_2 import short_tree
from cracking.chapter_4.p4_3 import list_of_depths, display


def num_paths(head: BNode, target: int) -> int:
    cum_sums = {}
    cur_sums = Counter({0: 1})
    total = 0

    def dfs(n: head, cum_sum=0):
        nonlocal total
        new_cs = cum_sums[n] = cum_sum + n.v
        cur_sums[new_cs] += 1
        print(new_cs - target, cur_sums)
        total += cur_sums[new_cs - target]
        if n.left:
            dfs(n.left, new_cs)
        if n.right:
            dfs(n.right, new_cs)
        cur_sums[new_cs] -= 1

    dfs(head)
    print(cum_sums)
    return total


def dfs():
    n = short_tree(list(range(15)))
    nodes = [n]
    res = []
    while nodes:
        cur = nodes.pop()
        if not cur:
            continue
        res.append(cur.v)
        nodes.append(cur.left)
        nodes.append(cur.right)
    print(' -> '.join(map(str, res)))


def preorder():
    n = short_tree(list(range(15)))
    def _order(n):
        if not n:
            return
        yield from _order(n.left)
        yield from _order(n.right)
        yield n.v
    print(' -> '.join(map(str, _order(n))))


def bfs():
    n = short_tree(list(range(15)))
    nodes = deque([n])
    res = []
    while nodes:
        cur = nodes.popleft()
        if not cur:
            continue
        res.append(cur.v)
        nodes.append(cur.left)
        nodes.append(cur.right)
    print(' -> '.join(map(str, res)))


def __main():
    dfs()
    preorder()
    return bfs()
    n = short_tree(list(range(15)))
    print(n)
    return
    n = short_tree(7 * [1])
    ll = list_of_depths(n)
    display(ll)
    print(30 * '=')

    print(n)
    print(num_paths(n, 2))
    pass


if __name__ == '__main__':
    __main()
