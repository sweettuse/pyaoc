__author__ = 'acushner'

from collections import Counter, defaultdict
from itertools import accumulate
from operator import itemgetter
from typing import NamedTuple


# 16.10 Living People: Given a list of people with their birth and death years, implement a method to
# compute the year with the most number of people alive. You may assume that all people were born
# between 1900 and 2000 (inclusive). If a person was alive during any portion of that year, they should
# be included in that year's count. For example, Person (birth= 1908, death= 1909) is included in the
# counts for both 1908 and 1909.
# Hints: #476, #490, #507, #514, #523, #532, #541, #549, #576

class Person(NamedTuple):
    birth: int
    death: int


def most_people(people: list[Person]) -> int:
    """return year with most living people"""
    births = Counter(p.birth for p in people)
    deaths = Counter(p.death + 1 for p in people)
    years = range(1900, 2001)
    living = accumulate(births[y] for y in years)
    dead = accumulate(deaths[y] for y in years)

    return max(zip(years, living, dead), key=lambda yld: yld[1] - yld[2])[0]


def most_people2(people: list[Person]) -> int:
    """return year with most living people"""
    births = Counter(p.birth for p in people)
    deaths = Counter(p.death + 1 for p in people)

    years = range(1900, 2001)
    alive = accumulate(births[y] - deaths[y] for y in years)

    return max(zip(years, alive), key=itemgetter(1))[0]


def most_people3(people: list[Person]) -> int:
    """return year with most living people"""
    alive = defaultdict(int)
    for p in people:
        alive[p.birth] += 1
        alive[p.death + 1] -= 1

    years = range(1900, 2001)
    living = accumulate(alive[y] for y in years)

    return max(zip(years, living), key=itemgetter(1))[0]


def __main():
    p = [
        Person(1900, 1901),
        Person(1900, 1901),
        Person(1910, 1990),
        Person(1970, 1990),
        Person(1974, 1990),
        Person(2001, 2016),
        Person(2001, 2016),
        Person(2001, 2016),
        Person(2001, 2016),
        Person(2001, 2016),
    ]
    print(most_people(p))
    print(most_people2(p))
    pass


if __name__ == '__main__':
    __main()
