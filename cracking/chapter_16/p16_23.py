__author__ = 'acushner'

# 16.23 Rand7 from Rands: Implement a method rand7() given rand5( ). That is, given a method that
# generates a random number between O and 4 (inclusive), write a method that generates a random
# number between O and 6 (inclusive).
# Hints:#505, #574, #637, #668, #697, #720
from collections import Counter
from random import randrange


def rand5():
    return randrange(5)


def rand7():
    return sum(rand5() for _ in range(7)) % 7


def rand7_2():
    while True:
        val = 5 * rand5() + rand5()
        if val < 21:
            return val % 7


from statistics import stdev, mean


def statisfy(f, times=20):
    res = []
    for _ in range(times):
        c = Counter(f() for _ in range(1400000))
        res.append(stdev(c.values()))
    print(mean(res))


def __main():
    statisfy(rand7)
    statisfy(rand7_2)
    return
    c = Counter(rand7() for _ in range(1400000))
    c2 = Counter(rand7_2() for _ in range(1400000))
    for kv in sorted(c.items()):
        print(kv)
    print(stdev(c.values()))
    print('==========')
    for kv in sorted(c2.items()):
        print(kv)
    print(stdev(c2.values()))


if __name__ == '__main__':
    __main()
