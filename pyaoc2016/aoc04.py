import string
from collections import Counter

__author__ = 'acushner'

from typing import NamedTuple, List

from cytoolz import first

from pyaoc2019.utils import read_file, exhaust

lowers = string.ascii_lowercase
t = 'aaaaa-bbb-z-y-x-123[abxyz]'
valids = set(lowers)


def _rotate_char(c, n):
    if c == '-':
        return ' '
    return lowers[(lowers.index(c) + n) % 26]


def _rotate_word(s, n):
    return ''.join(_rotate_char(c, n) for c in s)


class Room(NamedTuple):
    name: str
    sector_id: int
    checksum: str

    @classmethod
    def from_str(cls, s: str):
        checksum = s[-7:][1:-1]
        name, sector_id = s[:-7].rsplit('-', 1)
        return cls(name, int(sector_id), checksum)

    @property
    def calcd_checksum(self):
        c = Counter({k: v for k, v in Counter(self.name).items() if k in valids})
        res = sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))
        return ''.join(map(first, res[:5]))

    @property
    def is_real(self):
        return self.calcd_checksum == self.checksum

    @property
    def decrypted_name(self):
        return _rotate_word(self.name, self.sector_id)


def aoc04_a(rooms: List[Room]):
    return sum(r.sector_id for r in rooms if r.is_real)


def aoc04_b(rooms: List[Room]):
    name_sector_id = {r.decrypted_name: r.sector_id for r in rooms if r.is_real}
    return name_sector_id['northpole object storage']


def __main():
    rooms = [Room.from_str(s) for s in read_file(4, 2016)]
    print(aoc04_a(rooms))
    print(aoc04_b(rooms))


if __name__ == '__main__':
    __main()
