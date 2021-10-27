__author__ = 'acushner'


# https://leetcode.com/problems/count-numbers-with-unique-digits/

def count_nums_unique_digits(n):
    total = 0
    for s in map(str, range(10 ** n)):
        if len(set(s)) == len(s):
            total += 1
    return total

def __main():
    for i in range(1, 9):
        print(10 ** i, count_nums_unique_digits(i))


if __name__ == '__main__':
    __main()
