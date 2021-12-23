from collections import Counter, defaultdict
from dataclasses import dataclass
from itertools import count, islice

from pyaoc2019.utils import read_file, mapt
from typing import NamedTuple

__author__ = 'acushner'


def _dice():
    for i in count(1):
        yield i


def part1(p1, p2):
    players = [p1, p2]
    scores = [0, 0]
    turn = 0
    dice = _dice()

    def roll3():
        return islice(dice, 3)

    def move(start):
        dist = sum(roll3())
        return (start - 1 + dist) % 10 + 1

    while True:
        players[turn] = move(players[turn])
        scores[turn] += players[turn]

        if scores[turn] >= 1000:
            break
        turn ^= 1
    print(scores[turn ^ 1] * (next(dice) - 1))


def play():
    cur = [0]
    for _ in range(3):
        cur = [n + start for n in range(1, 4) for start in cur]
        print(len(cur))
        c = sorted(Counter(cur).items())
        for n, c in c:
            print(n, c, len(cur))

    # return cur



@dataclass
class PosSteps:
    pos: int = 0
    num_steps: int = 0


def play2(p1, p2):
    """need to know:

    each score needs list of :
        pos -> num_steps -> count
    """
    def score(pos):
        return (pos - 1) % 9 + 1

    move = score

    scores = [defaultdict(lambda: defaultdict(int)) for _ in range(25)]
    scores[0][p1][0] += 1
    for (i, pos_num_steps_map), _ in zip(enumerate(scores), range(3)):
        for roll in range(1, 4):
            new_score = score(i + roll)
            for cur_pos, num_steps in pos_num_steps_map.items():
                new_pos = move(cur_pos + roll)
                for ns, count in num_steps.items():
                    scores[new_score][new_pos][ns + 1] += count


    print(scores)
    for i, s in enumerate(scores):
        for k, v in s.items():
            print(i, v)





def part2(data):
    pass


def __main():
    p1, p2 = 1, 2
    # p1, p2 = 4, 8
    print(part1(p1, p2))
    play()
    print(play2(p1, p2))
    # print(part2(data))


if __name__ == '__main__':
    __main()
