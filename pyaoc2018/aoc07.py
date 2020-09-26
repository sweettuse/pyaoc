from collections import defaultdict
from operator import itemgetter
from typing import Dict

from pyaoc2019.utils import read_file, localtimer

import networkx as nx
from networkx.algorithms.dag import lexicographical_topological_sort, is_directed_acyclic_graph

__author__ = 'acushner'


def dagify():
    g = nx.DiGraph()
    for l in read_file(7, 2018):
        _, parent, *_, child, _, _ = l.split()
        g.add_edge(parent, child)
    return g


def part1():
    return ''.join(lexicographical_topological_sort(dagify()))


def _task_time(char):
    # ord('A') -> 65 and 'A' takes 61 seconds
    return ord(char) - 4


def part2():
    g = dagify()
    n_workers = 5
    in_progress: Dict[str, int] = {}
    total_time = 0
    while g:
        can_do = {t for t in g if not g.in_degree(t)} - in_progress.keys()
        if not can_do or len(in_progress) == n_workers:
            # need to wait for work to be completed
            tasks = sorted(in_progress.items(), key=itemgetter(1), reverse=True)
            t, task_time = tasks.pop()
            in_progress.pop(t)

            for k, v in in_progress.items():
                in_progress[k] -= task_time

            g.remove_node(t)
            total_time += task_time
        else:
            # ready to do some work
            for _, t in zip(range(n_workers - len(in_progress)), sorted(can_do)):
                in_progress[t] = _task_time(t)

    return total_time


def __main():
    order = part1()
    print(order)
    print(part2())


if __name__ == '__main__':
    __main()
