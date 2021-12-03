from pyaoc2019.utils import read_file, mapt

__author__ = 'acushner'

depths = mapt(int, read_file(1, 2021))


def part1(vals=depths):
    return sum(v2 > v1 for v2, v1 in zip(vals[1:], vals))


def part2():
    windowed = [sum(depths[i - 3: i]) for i in range(3, len(depths) + 1)]
    return part1(windowed)


def __main():
    print(part1())
    print(part2())


if __name__ == '__main__':
    __main()
