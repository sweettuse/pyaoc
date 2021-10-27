__author__ = 'acushner'

# 17.11 Word Distance: You have a large text file containing words. Given any two words, find the shortest
# distance (in terms of number of words) between them in the file. If the operation will be repeated
# many times for the same file (but different pairs of words), can you optimize your solution?
# Hints: #486, #501, #538, #558, #633
from bisect import bisect_left
from collections import defaultdict


class Book:
    def __init__(self, book: str):
        self._book = self._init_book(book)
        self._word_to_idxs = self._cache_word_idxs(self._book)

    @classmethod
    def _init_book(cls, book: str):
        return book.split()

    @staticmethod
    def _cache_word_idxs(book: list[str]) -> defaultdict[str, list[int]]:
        """index words to locations in text"""
        res = defaultdict(list)
        for idx, word in enumerate(book):
            res[word].append(idx)
        return res

    def find_min_distance(self, word1, word2):
        """return the minimum distance between words based on their idxs"""
        idxs1 = self._word_to_idxs[word1]
        idxs2 = self._word_to_idxs[word2]

        if not (idxs1 and idxs2):
            return

        if len(idxs1) > len(idxs2):
            idxs1, idxs2 = idxs2, idxs1

        min_dist = float('inf')
        for i1 in idxs1:
            i1_in_2 = bisect_left(idxs2, i1)
            if i1_in_2 > 0:
                min_dist = min(min_dist, abs(i1 - idxs2[i1_in_2 - 1]))
            if i1_in_2 != len(idxs2):
                min_dist = min(min_dist, abs(i1 - idxs2[i1_in_2]))

        return min_dist



def __main():
    book = 'it was the best of times it was the worst of times'
    b = Book(book)
    print(b.find_min_distance('best', 'worst'))
    pass


if __name__ == '__main__':
    __main()
