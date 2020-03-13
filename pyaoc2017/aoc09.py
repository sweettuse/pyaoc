from cytoolz.itertoolz import first

import pyaoc2019.utils as U

__author__ = 'acushner'

from enum import Enum


class State(Enum):
    not_garbage = 0
    inside = 1


def remove_garbage(s: str):
    state = State.not_garbage
    s = iter(s)
    total_garbage = 0

    for c in s:
        if state is State.inside:
            if c == '>':
                state = State.not_garbage
            elif c == '!':
                next(s)
            else:
                total_garbage += 1
        elif c == '<':
            state = State.inside

        elif state is State.not_garbage:
            yield c

    yield total_garbage


def aoc09(s):
    stack = []
    group_score = 0
    *cleaned_up, total_garbage = remove_garbage(s)
    for c in cleaned_up:
        if c == '{':
            stack.append(c)
        elif c == '}':
            group_score += len(stack)
            stack.pop()
    return group_score, total_garbage


def __main():
    data = first(U.read_file(9, 2017))
    print(aoc09(data))


if __name__ == '__main__':
    __main()
