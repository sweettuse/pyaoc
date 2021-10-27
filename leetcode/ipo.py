__author__ = 'acushner'


# https://leetcode.com/problems/ipo/

def maximize_capital(num_projects, starting_cap, profits, cost):
    cps = sorted(zip(cost, profits))
    return cps


def __main():
    k = 3
    w = 0
    profits = [1, 2, 3]
    capital = [0, 1, 2]
    print(maximize_capital(k, w, profits, capital))


if __name__ == '__main__':
    __main()
