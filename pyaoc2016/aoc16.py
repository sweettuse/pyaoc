from __future__ import annotations

from pyaoc2019.utils import timer


INPUT = '10010000000110000'


SWAP = {'1': '0', '0': '1'}

def _dragon_curve_slowest(seed: str):
    end = ''.join(SWAP[c] for c in reversed(seed))
    return f'{seed}0{end}'

def _dragon_curve_slower(seed: str):
    end = ''.join([SWAP[c] for c in reversed(seed)])
    return f'{seed}0{end}'


def dragon_curve(seed: str):
    end = ''.join(map(SWAP.__getitem__, reversed(seed)))
    return f'{seed}0{end}'


def checksum(binary: str | list[str]):
    while not len(binary) & 1:
        binary = ['1' if b0 == b1 else '0' for b0, b1 in zip(binary[::2], binary[1::2])]
    return ''.join(binary)


def _test_checksum():
    assert checksum('110010110100') == '100'


def _test_dragon_curve():
    assert dragon_curve('1') == '100'
    assert dragon_curve('0') == '001'
    assert dragon_curve('11111') == '11111000000'
    assert dragon_curve('111100001010') == '1111000010100101011110000'


@timer
def overwrite_data(seed: str, data_len: int, dc=dragon_curve):
    while len(seed := dc(seed)) < data_len:
        pass
    return checksum(seed[:data_len])


if __name__ == '__main__':
    _test_dragon_curve()
    _test_checksum()
    print('test:', overwrite_data('10000', 20))
    print('part 1:', overwrite_data(INPUT, 272))
    print('part 2:', overwrite_data(INPUT, 35651584, dragon_curve))

    print('WEIRD SLOWNESS')
    print('part 2 but slower:', overwrite_data(INPUT, 35651584, _dragon_curve_slower))
    print('part 2 but slowest:', overwrite_data(INPUT, 35651584, _dragon_curve_slowest))
