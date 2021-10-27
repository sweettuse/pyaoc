__author__ = 'acushner'

# 16.18 Pattern Matching: You are given two strings, pattern and value. The pattern string consists of
# just the letters a and b, describing a pattern within a string. For example, the string catcatgocatgo
# matches the pattern aabab (where cat is a and go is b). It also matches patterns like a, ab, and b.
# Write a method to determine if value matches pattern.
# Hints:#631, #643, #653, #663, #685, #718, #727


import re
from collections import Counter

A = '__AA__'
B = '__BB__'


def find_patterns(s):
    res = set()
    for l in range(1, len(s) + 1):
        a, rest = s[:l], s[l:]
        rest = set(rest.split(a)) - {''}
        if len(rest) > 1:
            continue

        if not rest:
            res.add(A)
        else:
            b = rest.pop()
            res.add(s.replace(a, A).replace(b, B))

    replace = lambda s, a_r, b_r: s.replace(a_r, 'a').replace(b_r, 'b')

    return {final for s in res
            for final in (replace(s, A, B), replace(s, B, A))}


def matches(s: str, pattern: str):
    print(find_patterns(s))
    return pattern in find_patterns(s)


def matches2(s: str, pattern: str):
    p = pattern
    if p.startswith('b'):
        # swap a's and b's
        p = p.replace('b', 't').replace('a', 'b').replace('t', 'a')

    counts = Counter(pattern)

    for a_l in range(1, len(s) + 1):
        b_l = (len(s) - counts['a'] * a_l) / counts['b']
        if not b_l.is_integer():
            continue

        b_l = int(b_l)
        a = b = None
        idx = 0
        res = True
        for cur_p in p:
            if cur_p == 'a':
                cur_a = s[idx: idx + a_l]
                if a is None:
                    a = cur_a
                elif a != cur_a:
                    res = False
                    break
                idx += a_l
            else:
                cur_b = s[idx: idx + b_l]
                if b is None:
                    b = cur_b
                elif b != cur_b:
                    res = False
                    break
                idx += b_l
        if res:
            final_s = ''.join((cur_b, cur_a)[cur_p == 'a'] for cur_p in p)
            print(final_s == s, final_s)
            print(cur_a, cur_b, )
            return True
    return False


def __main():
    s, p = 'catcatgocatgo', 'aabaab'
    s *= 2
    print(matches(s, p))
    print(matches2(s, p))
    pass


if __name__ == '__main__':
    __main()
