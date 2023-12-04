from __future__ import annotations
from dataclasses import dataclass

from pyaoc2019.utils import mapt, read_file


@dataclass(frozen=True)
class Card:
    id: int
    numbers: frozenset[int]
    winning: frozenset[int]
    num_matching: int

    @property
    def value(self) -> int:
        if self.num_matching == 0:
            return 0
        return 2 ** (self.num_matching - 1)

    @classmethod
    def from_str(cls, s: str) -> Card:
        id_str, rest = s.split(":")
        numbers_str, winning_str = rest.split("|")
        numbers, winning = map(cls._helper, (numbers_str, winning_str))
        return Card(
            int(id_str.split()[-1]),
            numbers,
            winning,
            len(numbers & winning),
        )

    @classmethod
    def _helper(cls, s: str) -> frozenset[int]:
        return frozenset(int(n) for n in s.split())


def part1(fname: str) -> int:
    return sum(card.value for card in _get_data(fname))


def part2(fname: str) -> int:
    cards = _get_data(fname)
    counts = dict.fromkeys((c.id for c in cards), 1)
    for c in cards:
        cur_count = counts[c.id]
        start_id = c.id + 1

        for id in range(start_id, start_id + c.num_matching):
            if id in counts:
                counts[id] += cur_count
            else:
                break
    return sum(counts.values())


def _get_data(fname) -> tuple[Card, ...]:
    return mapt(Card.from_str, read_file(fname))


def main():
    print(part1("04.txt"))
    print(part2("04.txt"))


if __name__ == "__main__":
    main()
