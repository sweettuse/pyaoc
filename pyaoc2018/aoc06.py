__author__ = 'acushner'

from collections import Counter
from operator import itemgetter

from pyaoc2019.colors.tile_utils import RC
from pyaoc2019.utils import read_file


def _manhattan(rc1, rc2):
    return abs(rc1.r - rc2.r) + abs(rc1.c - rc2.c)


def _get_min(rc, coms):
    t = sorted((_manhattan(rc, c), c) for c in coms)
    if t[0][0] != t[1][0]:
        return t[0][1]


def _get_total_dist(rc, coms):
    return sum(_manhattan(rc, c) for c in coms)


def parts1_and_2(coms):
    min_r, min_c = min(map(itemgetter(0), coms)), min(map(itemgetter(1), coms))
    max_r, max_c = max(map(itemgetter(0), coms)), max(map(itemgetter(1), coms))

    infinite = set()
    res = []
    total_close_to_all = 0
    for r_num in range(min_r, max_r + 1):
        r = []
        res.append(r)
        for c_num in range(min_c, max_c + 1):
            rc = RC(r_num, c_num)
            closest = _get_min(rc, coms)
            r.append(closest)
            if r_num in {min_r, max_r} or c_num in {min_c, max_c}:
                infinite.add(closest)
            if _get_total_dist(rc, coms) < 10000:
                total_close_to_all += 1

    counts = Counter(v for r in res for v in r if v not in infinite)
    return counts.most_common(1)[0][1], total_close_to_all


def __main():
    coms = [RC(*map(int, s.split(','))) for s in read_file(6, 2018)]
    print(parts1_and_2(coms))


if __name__ == '__main__':
    __main()
