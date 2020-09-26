from itertools import islice

from more_itertools import first

from pyaoc2019.utils import read_file

__author__ = 'acushner'

data = list(map(int, first(read_file(8, 2018)).split()))
# data = list(map(int, '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'.split()))


def part1():
    it = iter(data)

    def traverse():
        num_child, num_meta = islice(it, 2)
        return sum(traverse() for _ in range(num_child)) + sum(islice(it, num_meta))

    return traverse()


def part2():
    it = iter(data)

    def traverse():
        num_child, num_meta = islice(it, 2)
        values = [traverse() for _ in range(num_child)]
        meta = islice(it, num_meta)

        if not num_child:
            return sum(meta)

        return sum(values[idx - 1] for idx in meta if 0 < idx <= len(values))

    return traverse()


def __main():
    print(part1())
    print(part2())


if __name__ == '__main__':
    __main()
