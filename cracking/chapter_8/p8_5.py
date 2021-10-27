__author__ = 'acushner'


# 8.5  Recursive Multiply: Write a recursive function to multiply two positive integers without using the
# *operator.You can use addition, subtraction, and bit shifting, but you should minimize the number
# of those operations.

def simple(a, b):
    res = 0
    for _ in range(a):
        res += b
    return res


def rec_mult(a, b):
    def _helper(a, b, cur=0):
        if 0 in {a, b}:
            return 0
        if a == 1:
            return b + cur

        if a & 1:
            return _helper(a - 1, b, cur + b)
        else:
            return _helper(a >> 1, b << 1, cur)

    return _helper(*sorted((a, b)))


def rec_mult2(a, b):
    def _helper(a, b):
        if 0 in {a, b}:
            return 0
        if a == 1:
            return b

        if a & 1:
            return b + _helper(a - 1, b)
        else:
            return _helper(a >> 1, b << 1)

    return _helper(*sorted((a, b)))


def __main():
    nums = 100, 18
    print(simple(*nums))
    print(rec_mult(*nums))
    print(rec_mult2(*nums))
    pass


if __name__ == '__main__':
    __main()
