from collections import deque
from typing import Tuple, List, Union

from more_itertools import first

from pyaoc2019.utils import read_file, localtimer

__author__ = 'acushner'

STARTING_LAYOUT = 'abcdefghijklmnop'


def _parse_instruction(s: str) -> Tuple[str, List[str]]:
    return first(s), s[1:].split('/')


class Dance:
    """bust many moves"""

    def __init__(self, sl: str = STARTING_LAYOUT):
        self.layout = deque(sl)
        self._cmds = self._init_cmds()

    def _init_cmds(self):
        return dict(
            s=self._spin,
            x=self._exchange,
            p=self._partner,
        )

    def run(self, insts: List[str]):
        for cmd, args in map(_parse_instruction, insts):
            self._cmds[cmd](*args)

    def _spin(self, amount: str):
        """rotate the order of the programs"""
        self.layout.rotate(int(amount))

    def _exchange(self, *args: Union[int, str]):
        """swap positions based on index"""
        a, b = map(int, args)
        self.layout[a], self.layout[b] = self.layout[b], self.layout[a]

    def _partner(self, *args: str):
        """swap positions based on name"""
        self._exchange(*map(self.layout.index, args))


class DanceStr(Dance):
    def __init__(self, sl=STARTING_LAYOUT):
        super().__init__()
        self.layout = sl

    def _spin(self, amount: str):
        """rotate the order of the programs"""
        a = int(amount)
        self.layout = self.layout[-a:] + self.layout[:-a]

    def _exchange(self, *args: str):
        """swap positions based on index"""
        a, b = map(int, args)
        self._partner(self.layout[a], self.layout[b])

    def _partner(self, *args: str):
        """swap positions based on name"""
        a, b = args
        self.layout = self.layout.translate(str.maketrans({a: b, b: a}))


def part1(insts, n_times=1):
    d = Dance()
    for _ in range(n_times):
        d.run(insts)
    return ''.join(d.layout)


def part2(insts):
    configs = _find_all_configs(insts)
    return configs[int(1e9) % len(configs)]


def _find_all_configs(insts: List[str]) -> List[str]:
    """calculate all possible configs in cycle"""
    sl = STARTING_LAYOUT
    d = Dance(sl)
    res = [sl]
    while True:
        d.run(insts)
        cur = ''.join(d.layout)
        if cur == sl:
            return res
        res.append(cur)


def __main():
    insts = first(read_file(16, 2017)).split(',')
    with localtimer():
        print(part1(insts))
        print(part2(insts))


if __name__ == '__main__':
    __main()
