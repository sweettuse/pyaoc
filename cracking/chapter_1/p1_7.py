__author__ = 'acushner'


# 1.7 Rotate Matrix: Given an image represented by an NxN matrix, where each pixel in the image is 4
# bytes, write a method to rotate the image by 90 degrees. Can you do this in place?
# Hints: #51, # 100

def rotate(m):
    lm1 = len(m) - 1
    for layer_idx in range(0, (len(m) + 1) // 2):
        for j in range(len(m)):
            print(m[layer_idx][j], m[layer_idx + j][lm1 - j])
        return [[r[i] for r in reversed(m)] for i in range(len(m))]


def display(m):
    for r in m:
        print(r)


def __main():
    m = [[1, 2, 3],
         [4, 5, 6],
         [7, 8, 9]]
    display(rotate(m))


if __name__ == '__main__':
    __main()
