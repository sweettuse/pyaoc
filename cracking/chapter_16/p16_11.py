__author__ = 'acushner'


# 16.11 Diving Board: You are building a diving board by placing a bunch of planks of wood end-to-end.
# There are two types of planks, one of length shorter and one of length longer. You must use
# exactly K planks of wood. Write a method to generate all possible lengths for the diving board.
# Hints: #690, #700, #715, #722, #740, #747


def possible_lens(k):
    return [(i, k - i) for i in range(0, k + 1)]



def __main():
    print(possible_lens(4))
    pass


if __name__ == '__main__':
    __main()
