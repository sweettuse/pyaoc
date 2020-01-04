from cytoolz import first

from pyaoc2019.interpreter import parse_file, process_no_yield

__author__ = 'acushner'


def aoc2_a(p1, p2):
    instructions = parse_file(2)
    instructions[1:3] = p1, p2
    return first(process_no_yield(instructions))


def aoc2_b(target):
    return first(p1 * 100 + p2 for p1 in range(100) for p2 in range(100) if aoc2_a(p1, p2) == target)


def __main():
    print(aoc2_a(12, 2))
    print(aoc2_b(19690720))


if __name__ == '__main__':
    __main()
