__author__ = 'acushner'

# 4.1 Route Between Nodes: Given a directed graph, design an algorithm to find out whether there is a
# route between two nodes.
from collections import defaultdict, deque

from cracking.chapter_4 import Graph

adj_list = ['ab', 'ac', 'cd', 'df', 'fe', 'xy']


def path_from_to(g: Graph, start, end):
    for n in g.nodes:
        if n.name == start:
            break
    else:
        return False

    for c in n.bfs():
        if c.name == end:
            return True
    return False


def adj_list_find(al, start, end, dfs=True):
    """dfs"""
    if dfs:
        to_process = []
        pop = list.pop
    else:
        to_process = deque()
        pop = deque.popleft
    d = defaultdict(list)
    for cur, other in al:
        d[cur].append(other)

    if start not in d:
        return False

    to_process.extend(d.pop(start))
    while to_process:
        print(to_process)
        if (n := pop(to_process)) == end:
            return True
        to_process.extend(d.pop(n, []))

    return False


def __main():
    g = Graph.from_adj_list(adj_list)
    print(path_from_to(g, 'a', 'e'))
    print(adj_list_find(adj_list, 'a', 'e'))
    print(adj_list_find(adj_list, 'a', 'e', False))


if __name__ == '__main__':
    __main()
