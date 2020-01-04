from pyaoc2019.interpreter import parse_file, process_no_yield

__author__ = 'acushner'


def _aoc5(inp):
    return process_no_yield(parse_file(5, [inp])).output_register


def aoc5_a():
    return _aoc5(1)


def aoc5_b():
    return _aoc5(5)


def __main():
    print(aoc5_a())
    print(aoc5_b())


if __name__ == '__main__':
    __main()
