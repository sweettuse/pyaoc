from functools import partial
from operator import eq, lt, gt
from textwrap import dedent

from pyaoc2019.utils import read_file, mapt
from typing import NamedTuple

__author__ = 'acushner'


def parse_data(*, debug=False):
    prob_num = __file__[-5:-3]
    filename = int(prob_num)
    if debug:
        filename = f'{prob_num}.test'

    data = read_file(filename, 2015)

    def _parse_line(l):
        sue, rest = l.split(': ', maxsplit=1)
        n = int(sue[4:])
        return n, eval(f'dict({rest.replace(": ", "=")})')

    return dict(map(_parse_line, data))


def analyze():
    data = """children: 3
    cats: 7
    samoyeds: 2
    pomeranians: 3
    akitas: 0
    vizslas: 0
    goldfish: 5
    trees: 3
    cars: 2
    perfumes: 1"""

    def _process_line(l):
        l = l.strip()
        key, val = l.split(': ')
        return key, int(val)

    return dict(map(_process_line, data.splitlines()))


def _possible1(known_facts, aunt) -> bool:
    return all(v == known_facts[k] for k, v in aunt.items())


def _part_2_facts(known_facts):
    """> n cats and trees
    < n pomeranians and goldfish"""
    new_facts = {k: partial(eq, v) for k, v in known_facts.items()}
    new_facts['cats'] = lambda v: v > known_facts['cats']
    new_facts['trees'] = lambda v: v > known_facts['trees']
    new_facts['pomeranians'] = lambda v: v < known_facts['pomeranians']
    new_facts['goldfish'] = lambda v: v < known_facts['goldfish']
    return new_facts


def _possible2(new_facts, aunts):
    return all(new_facts[k](v) for k, v in aunts.items())


def parts1and2(aunts, pred_fn):
    return list(n for n, aunt in aunts.items() if pred_fn(aunt))


def part2(data):
    pass


def __main():
    aunts = parse_data(debug=False)
    known_facts = analyze()
    print(known_facts)
    print(aunts)
    print(parts1and2(aunts, partial(_possible1, known_facts)))
    print(parts1and2(aunts, partial(_possible2, _part_2_facts(known_facts))))


if __name__ == '__main__':
    __main()
