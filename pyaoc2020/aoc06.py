from functools import reduce

from pyaoc2019.utils import read_file, timer

__author__ = 'acushner'


def read_data():
    res = []
    cur = set()
    for l in read_file(6, 2020):
        if not l:
            res.append(cur)
            cur = set()
            continue

        cur.update(l)

    if cur:
        res.append(cur)

    return res


def read_data2():
    res = []
    cur = []
    for l in read_file(6, 2020):
        if not l:
            res.append(cur)
            cur = []
            continue
        cur.append(set(l))

    if cur:
        res.append(cur)

    return res


def part1():
    return sum(map(len, read_data()))


def part2():
    f = lambda v: reduce(set.intersection, v)
    return sum(map(len, map(f, read_data2())))


# ======================================================================================================================
# cleaned up to avoid code duplication
# ======================================================================================================================
def read_both(part_num=1):
    res = []
    cur = []
    for l in read_file(6, 2020):
        if not l:
            res.append(cur)
            cur = []
            continue

        cur.append(set(l))

    if cur:
        res.append(cur)

    f = set.union if part_num == 1 else set.intersection
    return (reduce(f, v) for v in res)


def both_parts(part_num=1):
    return sum(map(len, read_both(part_num)))


@timer
def __main():
    print(part1())
    print(part2())
    print(both_parts(1))
    print(both_parts(2))


if __name__ == '__main__':
    __main()
