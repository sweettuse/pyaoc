from contextlib import suppress
from hashlib import md5
from itertools import count, cycle
from operator import itemgetter

from cytoolz import take

from pyaoc2019.utils import localtimer

door_id = 'abc'

__author__ = 'acushner'

door_id = 'ffykfhsq'


def _gen_hash(door_id, next_every=100, next_func=None):
    for i in count():
        if next_func and not i % next_every:
            next(next_func)
        hexd = md5(f'{door_id}{i}'.encode()).hexdigest()
        if hexd.startswith('00000'):
            yield hexd


def aoc05_a():
    return ''.join(map(itemgetter(5), take(8, _gen_hash(door_id))))


def _fun_display(res):
    for r in cycle('-\\|/'):
        print('\r' * 8, end='')
        print(''.join(c or r for c in res), end='')
        yield


def aoc05_b():
    res = 8 * [None]
    disp = _fun_display(res)
    for hd in _gen_hash(door_id):
        try:
            idx = int(hd[5])
            if not res[idx]:
                res[idx] = hd[6]
                if all(res):
                    print('\r' * 8, end='')
                    return ''.join(res)
                next(disp)
        except (ValueError, IndexError):
            continue


def __main():
    # with localtimer():
    #     print(aoc05_a())
    with localtimer():
        print(aoc05_b())


if __name__ == '__main__':
    __main()
