__author__ = 'acushner'

# 16.5 Master Mind: The Game of Master Mind is played as follows:
# The computer has four slots, and each slot will contain a ball that is red (R). yellow (Y). green (G) or
# blue (B). For example, the computer might have RGGB (Slot #1 is red, Slots #2 and #3 are green, Slot
# #4 is blue).
# You, the user, are trying to guess the solution. You might, for example, guess YRGB.
# When you guess the correct color for the correct slot, you get a "hit:' If you guess a color that exists
# but is in the wrong slot, you get a "pseudo-hit:' Note that a slot that is a hit can never count as a
# pseudo-hit.
# For example, if the actual solution is RGBY and you guess GGRR, you have one hit and one pseudo-hit.
# Write a method that, given a guess and a solution, returns the number of hits and pseudo-hits.
# Hints:#639, #730
from collections import Counter, defaultdict
from enum import Enum
from typing import NamedTuple


class Color(Enum):
    R = 'r'
    Y = 'y'
    G = 'g'
    B = 'b'


class Hits(NamedTuple):
    hits: int
    pseudo: int


Colors = tuple[Color, Color, Color, Color]


def calc_hits(board: Colors, guess: Colors):
    num_hits = 0

    b_counts, g_counts = Counter(), Counter()
    for b, g in zip(board, guess):
        if b == g:
            num_hits += 1
        else:
            b_counts[b] += 1
            g_counts[g] += 1

    num_pseudo = sum((g_counts & b_counts).values())
    return Hits(num_hits, num_pseudo)


def __main():
    board = Color.R, Color.G, Color.B, Color.Y
    guess = Color.G, Color.G, Color.R, Color.R
    print(calc_hits(board, guess))


if __name__ == '__main__':
    __main()
