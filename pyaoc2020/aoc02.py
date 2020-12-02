from typing import NamedTuple

from pyaoc2019.utils import read_file, timer

__author__ = 'acushner'


class Policy(NamedTuple):
    min_n: int
    max_n: int
    letter: str
    password: str

    @classmethod
    def from_str(cls, s):
        rng, letter, pw = s.split()
        min_n, max_n = map(int, rng.split('-'))
        letter = letter[:-1]
        return cls(min_n, max_n, letter, pw)

    @property
    def is_valid(self):
        return self.min_n <= self.password.count(self.letter) <= self.max_n

    @property
    def is_valid2(self):
        return sum(self.password[i - 1] == self.letter for i in (self.min_n, self.max_n)) == 1


data = [Policy.from_str(s) for s in read_file(2, 2020)]


def part1():
    return sum(p.is_valid for p in data)


def part2():
    return sum(p.is_valid2 for p in data)


@timer
def __main():
    print(part1())
    print(part2())


if __name__ == '__main__':
    __main()
