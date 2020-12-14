from itertools import product

from cytoolz import memoize

from pyaoc2019.utils import read_file, timer

__author__ = 'acushner'

data = read_file(14, 2020)


def parse_data(fname=14, part_num=1):
    mask = None

    for inst, _, val in map(str.split, read_file(fname, 2020)):
        if inst.startswith('mask'):
            if part_num == 1:
                mask = [None if c == 'X' else c for c in val]
            else:
                mask = val
        else:
            addr, val = map(int, (inst[4:].replace(']', ''), val))
            yield mask, addr, val


def _to_bin(val):
    return bin(val)[2:].zfill(36)


def part1():
    mem = {}
    for mask, addr, val in parse_data():
        masked_val = ''.join(m or v for m, v in zip(mask, _to_bin(val)))
        mem[addr] = int(masked_val, 2)
    return sum(mem.values())


# ======================================================================================================================

def _calc_floating(addr):
    repeat = addr.count('X')
    addr = addr.replace('X', '{}')
    for vals in product((0, 1), repeat=repeat):
        yield int(addr.format(*vals), 2)


def part2():
    mem = {}
    for mask, addr, val in parse_data(part_num=2):
        bin_addr = _to_bin(addr)
        masked_addr = ''.join(a if m == '0' else m for a, m in zip(bin_addr, mask))

        if 'X' not in mask:
            mem[int(masked_addr, 2)] = val
            continue

        for float_addr in _calc_floating(masked_addr):
            mem[float_addr] = val

    return sum(mem.values())


@timer
def __main():
    print(part1())
    print(part2())


# 15018100062885
# 5724245857696
# '__main' took 0.09894214499999998 seconds


if __name__ == '__main__':
    __main()
