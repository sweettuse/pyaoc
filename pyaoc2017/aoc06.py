from itertools import zip_longest, count, repeat

from cytoolz.itertoolz import first

import pyaoc2019.utils as U

__author__ = 'acushner'


def get_data():
    return [int(v) for v in first(U.read_file(6, 2017)).split()]


def _find_max_and_idx(data):
    m = max(data)
    return m, data.index(m)


def reallocate(data, test=False):
    seen = {}
    cnt = count()
    while (td := tuple(data)) not in seen:
        seen[td] = next(cnt)
        m, idx = _find_max_and_idx(data)
        data[idx] = 0
        all_get, some_get = divmod(m, len(data))
        for i, extra in zip_longest(range(idx + 1, idx + len(data) + 1), repeat(1, some_get), fillvalue=0):
            data[i % len(data)] += all_get + extra

        if test:
            return data
    return len(seen), len(seen) - seen[td]


def run_tests():
    for t1, t2 in (([0, 4, 0], [1, 1, 2]),
                   ([0, 8, 0], [3, 2, 3]),
                   ([0, 10, 0], [3, 3, 4]),
                   ([0, 9, 0], [3, 3, 3]),
                   ([0, 4, 0, 0, 0], [1, 0, 1, 1, 1])):
        assert t2 == reallocate(t1, True)


def __main():
    data = get_data()
    run_tests()
    print(reallocate(data))


if __name__ == '__main__':
    __main()
