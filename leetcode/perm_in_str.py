__author__ = 'acushner'

# https://leetcode.com/problems/permutation-in-string/
from collections import deque, Counter


def perm_in_str(s1, s2):
    c = Counter(s2[:len(s1) - 1])
    s1c = Counter(s1)
    for i in range(len(s1) - 1, len(s2)):
        c[s2[i]] += 1
        if s1c == c:
            return True

        to_rm = s2[i - len(s1) + 1]

        c[to_rm] -= 1

        if not c[to_rm]:
            del c[to_rm]
    return False


def __main():
    s1 = "ab"
    s2 = "eidbaooo"
    print(perm_in_str(s1, s2))
    pass


if __name__ == '__main__':
    __main()
