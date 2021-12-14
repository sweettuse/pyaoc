from collections import Counter, defaultdict
from heapq import nlargest, nsmallest
from itertools import pairwise, combinations, product

from pyaoc2019.utils import read_file, mapt
from typing import NamedTuple

__author__ = 'acushner'


def parse_data(*, debug=False):
    prob_num = __file__[-5:-3]
    filename = int(prob_num)
    if debug:
        filename = f'{prob_num}.test'

    data = iter(read_file(filename, 2021))
    template = next(data)
    next(data)

    def _to_pi(l):
        pair, v = l.split(' -> ')
        return tuple(pair), v

    pi_map = dict(map(_to_pi, data))
    return template, pi_map


def _pair(t: tuple[str, str], repl):
    c1, c2 = t
    if t in repl:
        yield repl[t]
    yield c2


def _round(template, repl):
    return template[0] + ''.join(c for p in pairwise(template)
                                 for c in _pair(p, repl))


def part1(template, repl):
    for _ in range(10):
        template = _round(template, repl)
    vals = Counter(template).values()
    return nlargest(1, vals)[0] - nsmallest(1, vals)[0]


# ======================================================================================================================


def _count_elements(start, end, c):
    """start and end elements are undercounted, so need to add them back in"""
    res = defaultdict(int)
    for (c1, c2), num in c.items():
        res[c1] += num
        res[c2] += num

    for k, v in res.items():
        res[k] = v // 2

    res[start] += 1
    res[end] += 1

    return res


def _round2(pairs, repl):
    cur = defaultdict(int)
    for p, num in pairs.items():
        mid = repl[p]
        cur[p[0], mid] += num
        cur[mid, p[1]] += num
    return cur


def parts1and2(template, repl, num):
    pairs = Counter(pairwise(template))
    for _ in range(num):
        pairs = _round2(pairs, repl)

    counts = _count_elements(template[0], template[-1], pairs)
    return max(counts.values()) - min(counts.values())


def __main():
    template, repl = parse_data(debug=False)
    print(parts1and2(template, repl, 10))
    print(parts1and2(template, repl, 40))


if __name__ == '__main__':
    __main()
