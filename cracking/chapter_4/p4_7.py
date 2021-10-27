__author__ = 'acushner'

# 4.7  Build Order: You are given a list of projects and a list of dependencies (which is a list of pairs of
# projects, where the second project is dependent on the first project). All of a project's dependencies
# must be built before the project is. Find a build order that will allow the projects to be built. If there
# is no valid build order, return an error.
# EXAMPLE
# Input:
# projects: a, b, c, d, e, f
# dependencies: (a, d), (f, b), (b, d), (f, a), (d, c)
# Output: f, e, a, b, d, c
# Hints: #26, #47, #60, #85, #725, #133
from collections import defaultdict, deque, Counter
from functools import lru_cache

from cracking.chapter_4 import Graph


class Node:
    def __init__(self, name):
        self.name = name
        self.mark = None

    def __str__(self):
        return f'Node({self.name})'

    __repr__ = __str__


@lru_cache
def _get_node(s):
    return Node(s)


def _to_dict(nodes, adj_list):
    nodes = set(map(_get_node, nodes))
    deps = defaultdict(set)

    for k, v in adj_list:
        k, v = _get_node(k), _get_node(v)
        deps[k].add(v)

    deps_counter = Counter(v for vals in deps.values() for v in vals)
    for n in nodes - deps.keys():
        deps[n] = set()
    return nodes, deps, deps_counter


def create_build_order(nodes, adj_list):
    nodes, deps, counts = _to_dict(nodes, adj_list)

    to_process = list(set(deps) - set().union(*deps.values()))
    res = []
    while to_process:
        k = to_process.pop()
        res.append(k)
        downstream = deps.pop(k, [])
        for d in downstream:
            if counts[d] == 1:
                to_process.append(d)
            counts[d] -= 1

    if deps:
        return False
    return res



def __main():
    deps = 'ad', 'fb', 'bd', 'fa', 'dc'
    print(create_build_order('eabcdf', deps))
    pass


if __name__ == '__main__':
    __main()
