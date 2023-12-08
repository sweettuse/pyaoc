from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
from functools import cached_property
from itertools import count

from pyaoc2019.utils import mapt, read_file, timer


CARD_VALS = dict(zip("23456789TJQKA", count(1)))
CARD_VALS2 = CARD_VALS | dict(J=0)


@dataclass(frozen=True)
class Hand:
    cards: str
    bid: int

    @classmethod
    def from_str(cls, s: str) -> Hand:
        cards, bid = s.split()
        return cls(cards.strip(), int(bid))

    def _type_rank(self, cards: str) -> int:
        counts = sorted(Counter(cards).values())
        match counts:
            case [5]:  # five of a kind
                return 7
            case [1, 4]:  # four of a kind
                return 6
            case [2, 3]:  # full house
                return 5
            case [1, 1, 3]:  # three of a kind
                return 4
            case [1, 2, 2]:  # two pair
                return 3
            case [1, 1, 1, 1, 1]:  # high card
                return 1
            case _:  # one pair
                return 2

    def _cards_rank(self) -> tuple[int, ...]:
        return tuple(CARD_VALS[c] for c in self.cards)  # type: ignore

    @cached_property
    def rank(self) -> tuple[int, tuple[int, ...]]:
        return self._type_rank(self.cards), self._cards_rank()

    def __lt__(self, other: Hand) -> bool:
        return self.rank < other.rank

    def __eq__(self, other: Hand) -> bool:
        return self.rank == other.rank


@dataclass(frozen=True)
class Hand2(Hand):
    def _type_rank(self, cards: str) -> int:
        num_js = cards.count("J")
        if num_js == 5:
            cards = "AAAAA"
        elif num_js == 4:
            cards = cards.replace("J", "") * 5
        elif num_js:
            no_js = cards.replace("J", "")
            to_try = (cards.replace("J", c) for c in no_js)
            cards = max(to_try, key=self._type_rank)

        return super()._type_rank(cards)

    def _cards_rank(self) -> tuple[int, ...]:
        return tuple(CARD_VALS2[c] for c in self.cards)


def part1() -> int:
    return _parts1_and_2("07.txt", Hand)


def part2() -> int:
    return _parts1_and_2("07.txt", Hand2)


def _parts1_and_2(fname, cls):
    cards = sorted(_get_data(fname, cls))
    return sum(c.bid * mul for c, mul in zip(cards, count(1)))


def _get_data(fname, cls=Hand) -> tuple[Hand, ...]:
    return mapt(cls.from_str, read_file(fname))


def main():
    print(part1())
    print(part2())


if __name__ == "__main__":
    main()
