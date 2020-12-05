from pyaoc2019.utils import read_file, timer

__author__ = 'acushner'

bin_map = dict(F=0, L=0, B=1, R=1)


def to_num(s):
    return int(''.join(map(str, (bin_map[c] for c in s))), 2)


data = {to_num(v) for v in read_file(5, 2020)}


def part1():
    return max(data)


def part2():
    min_seat, max_seat = min(data), max(data)
    valid_nums = set(range(min_seat + 8, max_seat - 7))
    return (valid_nums - data).pop()


@timer
def __main():
    print(part1())
    print(part2())


if __name__ == '__main__':
    __main()
