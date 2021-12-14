from itertools import permutations, starmap, pairwise

from pyaoc2019.utils import read_file

__author__ = 'acushner'


def parse_data(*, debug=False):
    prob_num = __file__[-5:-3]
    filename = int(prob_num)
    if debug:
        filename = f'{prob_num}.test'

    locs = set()

    def _to_record(l):
        a, _, b, _, dist = l.split()
        locs.add(a)
        locs.add(b)
        return _sort_tuple(a, b), int(dist)

    return locs, dict(map(_to_record, read_file(filename, 2015)))


def _sort_tuple(*args):
    return tuple(sorted(args))


def parts1and2(locs, dists, agg):
    return agg(sum(dists[c]
                   for c in starmap(_sort_tuple, pairwise(p)))
               for p in permutations(locs))


def __main():
    locs, dists = parse_data(debug=False)
    print(parts1and2(locs, dists, min))
    print(parts1and2(locs, dists, max))


if __name__ == '__main__':
    __main()
