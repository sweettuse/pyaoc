from contextlib import suppress
from functools import partial
from itertools import islice, count
from math import prod
from operator import gt, lt, eq

from pyaoc2019.utils import read_file, mapt
from typing import NamedTuple

__author__ = 'acushner'


def parse_data(*, debug=False):
    prob_num = __file__[-5:-3]
    filename = int(prob_num)
    if debug:
        filename = f'{prob_num}.test'

    data = read_file(filename, 2021)
    line = data[0]
    res = _to_bits(line)
    assert len(line) * 4 == len(res), (len(res) - len(line) * 4)
    return res


hex_to_bits = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',
}


def _to_bits(s):
    return ''.join(hex_to_bits[c] for c in s)


def _take(it, n):
    res = ''.join(islice(it, n))
    if len(res) != n:
        raise ValueError(f'take exhausted early {n - len(res)} missing chars')
    return res


def int2(s):
    return int(s, 2)


version_sum = 0


def parse(bits, num_packets=None):
    global version_sum
    version_sum = 0
    return _parse(bits, num_packets)


def _parse(bits, num_packets=None):
    global version_sum
    bits = iter(bits)
    rng = range(num_packets) if num_packets else count()
    take = partial(_take, bits)

    def _parse_literal():
        res = []
        while True:
            s = take(5)
            res.extend(s[1:])
            if s.startswith('0'):
                break
        return int2(''.join(res))

    def _parse_operator():
        l = take(1)
        if l == '0':
            num_bits = int2(take(15))
            return _parse(take(num_bits))
        else:
            num_packets = int2(take(11))
            return _parse(bits, num_packets)

    stack = []
    for _ in rng:
        try:
            version, type = int2(take(3)), int2(take(3))
            version_sum += version
            match type:
                case 4:  # literal
                    stack.append(_parse_literal())
                case op:  # operator
                    stack.append((op, _parse_operator()))

        except ValueError:
            break

    return stack


def _test():
    def _basic(s, r):
        res = parse(s)
        assert res == r, (res, r)

    _basic('110100101111111000101000', [2021])
    _basic('00111000000000000110111101000101001010010001001000000000', [(6, [10, 20])])
    _basic('11101110000000001101010000001100100000100011000001100000', [(3, [1, 2, 3])])

    def _check_version(s, n):
        res = parse(_to_bits(s))
        assert version_sum == n, (s, version_sum, n, res)

    _check_version('8A004A801A8002F478', 16)
    _check_version('620080001611562C8802118E34', 12)
    _check_version('C0015000016115A2E0802F182340', 23)
    _check_version('A0016C880162017C3686B18A3D4780', 31)


def part1(bits):
    t = parse(bits)
    return version_sum


def part2(bits):
    instructions = parse(bits)
    bind = lambda fn: lambda *args: fn(args)
    funcs = {
        0: bind(sum),
        1: bind(prod),
        2: bind(min),
        3: bind(max),
        5: gt,
        6: lt,
        7: eq,
    }

    def _parse_cmd(inst):
        cmd, args = inst
        return funcs[cmd](*_parse_args(*args))

    def _parse_args(*args):
        for a in args:
            if isinstance(a, int):
                yield a
            else:
                yield _parse_cmd(a)

    return _parse_cmd(instructions[0])


def __main():
    _test()
    bits = parse_data(debug=False)
    print(part1(bits))
    print(part2(bits))


if __name__ == '__main__':
    __main()
