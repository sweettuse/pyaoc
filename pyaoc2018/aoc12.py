from collections import defaultdict

from more_itertools import last, first

from pyaoc2019.utils import read_file, localtimer, exhaust

__author__ = 'acushner'


def init_state_and_state_map():
    f = iter(read_file(12, 2018))
    init_state = next(f).strip().split()[-1]
    next(f)
    lines = (l.strip().split() for l in f)
    state_map = {state: output for state, _, output in lines}
    return init_state, state_map


def _add_empties(n, state):
    empties = n * '.'
    return n, f'{empties}{state}{empties}'


def _simulate(state, state_map):
    while True:
        res = (state_map[state[i - 2:i + 3]] for i in range(2, len(state) - 2))
        state = f'..{"".join(res)}..'
        yield state


def _score(state, offset):
    return sum(i - offset for i, c in enumerate(state) if c == '#')


def part1(init_state, state_map, num_gen=20):
    offset, state = _add_empties(40, init_state)
    for _, state in zip(range(num_gen), _simulate(state, state_map)):
        pass
    return _score(state, offset)


def part2(init_state, state_map):
    def cache_state(s):
        starting = s.index('#')
        s = s[starting: s.rindex('#') + 1]
        s_in_cache = s in cache
        cache[s].append(starting)
        if s_in_cache:
            return True

    offset, state = _add_empties(15000, init_state)
    cache = defaultdict(list)
    cache_state(state)

    for next_state in _simulate(state, state_map):
        if cache_state(next_state):
            break

    final_state = last(cache.keys())
    exhaust(print, enumerate(cache.values()))
    num_gen = 50_000_000_000
    first_150 = 80
    final_offset = - first_150 - (num_gen - 150)
    return _score(final_state, final_offset)


def __main():
    init_state, state_map = init_state_and_state_map()
    print(part1(init_state, state_map))
    with localtimer():
        print('===============')
        print(part2(init_state, state_map))
    print(50000000000 - 50_000_000_000)


if __name__ == '__main__':
    __main()
