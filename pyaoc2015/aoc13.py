from functools import partial
from itertools import permutations

from pyaoc2019.utils import read_file, mapt
from typing import NamedTuple

__author__ = 'acushner'


def parse_data(*, debug=False):
    prob_num = __file__[-5:-3]
    filename = int(prob_num)
    if debug:
        filename = f'{prob_num}.test'

    def _parse_line(l):
        t = l.split()
        return (t[0], t[-1][:-1]), (2 * (t[2] == 'gain') - 1) * int(t[3])

    happiness = dict(map(_parse_line, read_file(filename, 2015)))
    seen = set()
    people = [k[0] for k in happiness if k[0] not in seen and not seen.add(k[0])]
    return people, happiness


def _score(people, happiness):
    total = 0
    num_peeps = len(people)
    for i in range(num_peeps):
        total += happiness[people[i], people[i - 1]]
        total += happiness[people[i], people[(i + 1) % num_peeps]]
    return total


def part1(people, happiness):
    score = partial(_score, happiness=happiness)
    best_score = max(map(score, permutations(people)))
    return best_score


def part2(people, happiness):
    me = 'jebtuse'
    h = happiness.copy()
    for p in people:
        h[me, p] = 0
        h[p, me] = 0
    return part1(people + [me], h)

def __main():
    people, happiness = parse_data(debug=False)
    print(part1(people, happiness))
    print(part2(people, happiness))


if __name__ == '__main__':
    __main()
