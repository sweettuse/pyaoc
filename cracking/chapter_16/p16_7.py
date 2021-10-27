__author__ = 'acushner'


# 16.7 Number Max: Write a method that finds the maximum of two numbers. You should not use if-else
# or any other comparison operator.
# Hints: #473, #513, #707, #728

def number_max(a, b):
    idx = ((a - b) >> 64) + 1
    return (a, b)[idx ^ 1]


def __main():
    print(number_max(4, 6))
    pass


if __name__ == '__main__':
    __main()
