__author__ = 'acushner'

# 1.5 One Away: There are three types of edits that can be performed on strings: insert a character,
# remove a character, or replace a character. Given two strings, write a function to check if they are
# one edit (or zero edits) away.
# EXAMPLE
# pale, ple -> true
# pales, pale -> true
# pale, bale -> true
# pale, bake -> false
# Hints:#23, #97, #130
from collections import Counter


def can_replace_one(s1, s2):
    num_diffs = 0
    for c1, c2 in zip(s1, s2):
        if c1 != c2:
            num_diffs += 1
            if num_diffs > 1:
                return False
    return True


def can_add_one(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1
    j_offset = 0
    for i in range(len(s1)):
        if s1[i] != s2[i + j_offset]:
            j_offset += 1
            if j_offset > 1:
                return False
    return True


def are_close(s1, s2):
    if s1 == s2:
        return True

    if len(s1) == len(s2):
        return can_replace_one(s1, s2)

    if abs(len(s1) - len(s2)) > 1:
        return False

    return can_add_one(s1, s2)


def __main():
    print(are_close('azcd', 'abqd'))
    for ss in (('pale', 'ple'),
               ('pales', 'pale'),
               ('pale', 'bale'),
               ('pale', 'bales'),
               ('pale', 'bake'),):
        print(ss, are_close(*ss))

    pass


if __name__ == '__main__':
    __main()
