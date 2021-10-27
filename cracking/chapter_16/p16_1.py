__author__ = 'acushner'


# 16.1 Number Swapper: Write a function to swap a number in place (that is, without temporary variables).
# Hints: #492, #715, #736
def swap1(a, b):
    a, b = b, a
    print(a, b)


def swap2(a, b):
    a ^= b
    b ^= a
    a ^= b
    print(a, b)


def swap_bit(a, b):
    1, 0


    pass

def __main():
    a, b = 4, 61
    print(swap1(a, b))
    print(swap2(a, b))
    pass


if __name__ == '__main__':
    __main()
