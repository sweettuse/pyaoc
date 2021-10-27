# https://leetcode.com/problems/decode-ways/
from itertools import chain

# '10' -> 'j'
# '11' -> 'aa'; 'k'
# '1110' -> '60111'
from typing import Iterator


def _val(c: str):
    if c in set('123456789'):
        return 1
    if c == '*':
        return 9


def decode(s: str):
    if not s:
        return 1
    l, *first = s
    if l == '0':
        return decode(''.join(first[1:]))

    if not first:
        return 1

    s, *first_2 = first
    if s in '12':
        return decode(''.join(first)) + decode(''.join(first_2))
    return decode(''.join(first))


def decode2(s: str):
    score = [0] * (len(s) + 1)
    score[0] = score[1] = 1

    if s[0] == "0":
        return 0

    for i in range(2, len(s) + 1):
        if 1 <= int(s[i - 1]) <= 9:
            score[i] += score[i - 1]
        if 10 <= int(s[i - 2:i]) <= 26:
            score[i] += score[i - 2]
        print(s[i - 1], score)
    return score[-1]


def __main():
    print(decode2('3231'))
    print(decode2('1229374882931111111111111111111'))


coins = [1, 5, 10, 25]

if __name__ == '__main__':
    __main()
