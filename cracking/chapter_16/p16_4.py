__author__ = 'acushner'


# 16.4 Tic Tac Win: Design an algorithm to figure out if someone has won a game of tic-tac-toe.
# Hints:#710, #732

def has_won(board: list[list[int]]) -> bool:
    def _has_won(vals):
        vals = set(vals)
        print(vals)
        return len(vals) == 1 and vals.pop() in {'x', 'o'}

    print(board)

    def _get_vals_to_check():
        yield from board
        l = len(board)
        yield from ((board[r][c] for r in range(l)) for c in range(l))
        yield (board[c][c] for c in range(l))
        yield (board[c][-1 - c] for c in range(l))

    return any(map(_has_won, _get_vals_to_check()))


def __main():
    board = [['x', 'o', 'x'],
             ['x', 'o', 6],
             ['x', 8, 'o']]
    print(has_won(board))

    pass


if __name__ == '__main__':
    __main()
