__author__ = 'acushner'

from collections import deque, defaultdict

num_players = 468
last_marble = 71843

# num_players = 30
# last_marble = 5807


def parts1and2(mult=1):
    circle = deque([2, 1, 0])
    scores = defaultdict(int)
    for n in range(3, mult * last_marble + 1):
        if not n % 23:
            player = n % num_players
            circle.rotate(7)
            scores[n % num_players] += n + circle.popleft()
            'edge case'
        else:
            circle.rotate(-2)
            circle.appendleft(n)
    return max(scores.values())


def __main():
    print(parts1and2())
    print(parts1and2(100))
    pass


if __name__ == '__main__':
    __main()
