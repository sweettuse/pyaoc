from functools import lru_cache

from pyaoc2019.utils import read_file, timer

__author__ = 'acushner'

# data = sorted((int(v) for v in read_file('10.test', 2020)), reverse=True)
# data = sorted((int(v) for v in read_file('10.test2', 2020)), reverse=True)
data = sorted((int(v) for v in read_file(10, 2020)), reverse=True)
data = [data[0] + 3] + data + [0]


def part1():
    diffs = [v1 - v2 for v1, v2 in zip(data, data[1:])]
    return sum(d == 1 for d in diffs) * sum(d == 3 for d in diffs)


def part2():
    conns = list(reversed(data))

    def _direct_conns(idx):
        return [cur for cur in range(idx - 4, idx)
                if cur >= 0 and conns[cur] >= conns[idx] - 3]

    @lru_cache
    def _num_sub_conns(idx=len(conns) - 1):
        if idx <= 1:
            return 1
        directs = _direct_conns(idx)
        return sum(map(_num_sub_conns, directs))

    return _num_sub_conns()


@timer
def __main():
    print(part1())
    print(part2())


# 1625
# 3100448333024
# '__main' took 0.0003900200000000048 seconds


if __name__ == '__main__':
    __main()
