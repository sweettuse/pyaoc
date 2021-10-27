__author__ = 'acushner'

# https://leetcode.com/problems/find-all-anagrams-in-a-string
from collections import Counter


def find_anagrams(s, p):
    p_count = Counter(p)
    p_len = len(p)
    acc = Counter(s[:p_len - 1])
    res = []

    for right in range(p_len - 1, len(s)):
        left = right - p_len + 1
        acc[s[right]] += 1
        if acc == p_count:
            res.append(left)

        to_rm = s[left]
        if to_rm in acc:
            acc[to_rm] -= 1
            if not acc[to_rm]:
                del acc[to_rm]

    return res


def __main():
    s = "abab"
    p = "ab"
    print(find_anagrams(s, p))


if __name__ == '__main__':
    __main()
