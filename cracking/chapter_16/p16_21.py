__author__ = 'acushner'


# 16.21 Sum Swap: Given two arrays of integers, find a pair of values (one value from each array) that you
# can swap to give the two arrays the same sum.
# EXAMPLE
# Input: {4, 1, 2, 1, 1, 2} and {3, 6, 3, 3}
# Output: {1, 3}
# Hints: #545, #557, #564, #577, #583, #592, #602, #606, #635


def check(sum1, sum2, v1, v2):
    print('check', sum1 - v1 + v2, sum2 - v2 + v1)


def sum_swap(l1, l2):
    sum1, sum2 = map(sum, (l1, l2))
    s1, s2 = map(set, (l1, l2))
    target = sum1 - sum2
    for n1 in s1:
        if target - n1 in s2:
            check(sum1, sum2, n1, target - n1)
            return n1, target - n1
        # if -target - n1 in s2:
        #     check(sum1, sum2, n1, -target - n1)
        #     return n1, -target - n1


def sum_swap2(l1, l2):
    # sum1 - v1 + v2 = sum2 + v1 - v2
    # sum1 - sum2 = 2 * (v1 - v2)
    # (sum1 - sum2) / 2 = v1 - v2
    # v1 - v2 = target
    # v1 - target = v2

    sum1, sum2 = map(sum, (l1, l2))
    if (sum1 + sum2) & 1:
        return

    s1, s2 = map(set, (l1, l2))
    target = (sum1 - sum2) // 2
    for v1 in s1:
        if (v2 := v1 - target) in s2:
            check(sum1, sum2, v1, v2)
            return v1, v2


def __main():
    l1, l2 = [4, 1, 2, 1, 1, 2], [3, 6, 3, 3]
    l1 = [0, -1, 0, 0]
    l2 = [0, -2, 0, -1]
    # l1 = [-v for v in l1]
    # l2 = [-v for v in l2]
    print(sum_swap(l1, l2))
    print('============')
    print(sum_swap2(l1, l2))


if __name__ == '__main__':
    __main()
