
from operator import inv, lshift, rshift, and_, or_

from pyaoc2019.utils import read_file, timer

__author__ = 'acushner'


def parse_data(*, debug=False):
    prob_num = __file__[-5:-3]
    filename = int(prob_num)
    if debug:
        filename = f'{prob_num}.test'

    def to_int_maybe(v):
        try:
            return int(v)
        except:
            return v

    funcs = dict(AND=lambda a, b: and_(a, b) & 0xFFFF,
                 OR=lambda a, b: or_(a, b) & 0xFFFF,
                 LSHIFT=lambda a, b: lshift(a, b) & 0xFFFF,
                 RSHIFT=lambda a, b: rshift(a, b) & 0xFFFF)

    def invert(v):
        return inv(v) & 0xFFFF

    def _get_circuit(l):
        left, right = l.split(' -> ')
        match left.split():
            case ('NOT', x):
                left = invert, to_int_maybe(x)
            case x, cmd, y:
                left = funcs[cmd], to_int_maybe(x), to_int_maybe(y)
            case (x, ):
                left = to_int_maybe(x)
            case _:
                raise Exception('wth')
        return left, to_int_maybe(right)

    return [_get_circuit(l) for l in read_file(filename, 2015)]


class Circuit:
    def __init__(self, data):
        self._funcs = {}
        self._parse_data(data)

    @lru_cache(None)
    def get(self, s):
        if isinstance(s, str):
            return self._funcs[s]()
        return s

    def _parse_data(self, data):
        funcs = self._funcs

        for i, o in data:
            if isinstance(i, int):
                funcs[o] = lambda i=i: i
            elif isinstance(i, str):
                funcs[o] = lambda i=i: self.get(i)
            else:
                fn, *args = i
                funcs[o] = lambda fn=fn, args=args: fn(*map(self.get, args))


@timer
def part1(data):
    c = Circuit(data)
    return c.get('a')


def part2(data, b_override):
    c = Circuit(data)
    c._funcs['b'] = lambda: b_override
    return c.get('a')


def __main():
    data = parse_data(debug=False)
    # exhaust(print, data)
    print(orig_a := part1(data))
    print(part2(data, orig_a))


if __name__ == '__main__':
    __main()
