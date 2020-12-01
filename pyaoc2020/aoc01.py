from pyaoc2019.utils import read_file

__author__ = 'acushner'

data = frozenset(map(int, read_file(1, 2020)))


def part1(target=2020):
    for n in data:
        if (other := target - n) in data:
            return n * other


def part2():
    for n in data:
        if (other := part1(2020 - n)) is not None:
            return n * other


def __main():
    print(part1())
    print(part2())


if __name__ == '__main__':
    __main()
