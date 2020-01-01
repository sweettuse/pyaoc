import pytest
from cytoolz import first, last

from pyaoc2019.interpreter import parse_file, parse_data, process

__author__ = 'acushner'


def aoc2(p1, p2):
    data = parse_file('02')
    data[1:3] = p1, p2
    return first(process(data))


def aoc2_b(target):
    return first(p1 * 100 + p2 for p1 in range(100) for p2 in range(100) if aoc2(p1, p2) == target)


class Test:
    def test2(self):
        assert aoc2(12, 2) == 4930687
        assert aoc2_b(19690720) == 5335

    def test5a(self):
        assert last(process(parse_data('1101,100,-1,4,0'))) == 99
        assert last(process(parse_data('1002,4,3,4,33'))) == 99
        assert process(parse_file(5, [1])).output_register == 15259545

    def test5b(self):
        for data in ('3,9,8,9,10,9,4,9,99,-1,8', '3,3,1108,-1,8,3,4,3,99'):
            assert process(parse_data(data, [2])).output_register == 0
            assert process(parse_data(data, [8])).output_register == 1

        assert process(parse_data('3,3,1107,-1,8,3,4,3,99', [9])).output_register == 0
        assert process(parse_data('3,3,1107,-1,8,3,4,3,99', [-2])).output_register == 1

        data = '3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99'
        assert process(parse_data(data, [8])).output_register == 1000
        assert process(parse_data(data, [-4928])).output_register == 999
        assert process(parse_data(data, [4928])).output_register == 1001
        assert process(parse_file(5, [5])).output_register == 7616021





def __main():
    pass


if __name__ == '__main__':
    __main()
