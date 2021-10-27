__author__ = 'acushner'


def sign(n):
    return -1 if n < 0 else 1


def flip(n):
    """pos -> neg and vice versa"""
    cur_sign = -sign(n)
    res = 0
    while n != 0:
        res += cur_sign
        n += cur_sign
    return res


def abs(n):
    if n < 0:
        return flip(n)
    return n


def subtract(a, b):
    return a + flip(b)


def multiply(a, b):
    do_flip = sign(a) + sign(b) == 0
    a = abs(a)
    b = abs(b)
    a, b = sorted((a, b), reverse=True)

    res = 0

    for _ in range(b):
        res += a

    return flip(res) if do_flip else res


def divide(a, b):
    do_flip = sign(a) + sign(b) == 0
    a = abs(a)
    b = abs(b)
    res = 0
    while a >= b:
        a = subtract(a, b)
        res += 1

    if a and do_flip:
        res += 1

    return flip(res) if do_flip else res


def __main():
    print(subtract(-21, 6))
    print(multiply(1998, 10000000000))
    print(divide(-8, 3))


if __name__ == '__main__':
    __main()
