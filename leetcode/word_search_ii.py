__author__ = 'acushner'


# https://leetcode.com/problems/word-search/

class Board:
    def __init__(self, board: list[str]):
        self.board = [list(b) for b in board]

    def __str__(self):
        return '\n'.join(map(str, self.board))

    def _is_valid(self, r, c):
        return 0 <= r < len(self.board) and 0 <= c < len(self.board[0])

    def _get_adj(self, r, c):
        res = set()
        for r_o, c_o in (0, 1), (1, 0), (0, -1), (-1, 0):
            if self._is_valid(r + r_o, c + c_o):
                res.add((r + r_o, c + c_o))
        return res

    def find(self, word):
        seen = set()
        word = list(word)

        def _find(r, c, w_idx=0):
            try:
                seen.add((r, c))

                if word[w_idx] == self.board[r][c]:
                    if w_idx == len(word) - 1:
                        return True
                    return any(_find(r1, c1, w_idx + 1) for r1, c1 in self._get_adj(r, c) - seen)

            finally:
                seen.remove((r, c))

        for r_idx, row in enumerate(self.board):
            for c_idx, v in enumerate(row):
                if v == word[0] and _find(r_idx, c_idx):
                    return True
        return False


def __main():
    board = [['o', 'a', 'a', 'n'], ['e', 't', 'a', 'e'], ['i', 'h', 'k', 'r'], ['i', 'f', 'l', 'v']]
    words = ['oath', 'pea', 'eat', 'rain']

    board = [['A', 'B', 'C', 'E'], ['S', 'F', 'C', 'S'], ['A', 'D', 'E', 'E']]
    word = 'ABCCED'
    board = [["A", "A", "A", "A", "A", "A"], ["A", "A", "A", "A", "A", "A"], ["A", "A", "A", "A", "A", "A"],
             ["A", "A", "A", "A", "A", "A"], ["A", "A", "A", "A", "A", "B"], ["A", "A", "A", "A", "B", "A"]]
    word = "AAAAAAAAAAAAABB"
    b = Board(board)
    print(b)
    print(b.find(word))


if __name__ == '__main__':
    __main()
