__author__ = 'acushner'


# 1.9 String Rotation: Assume you have a method isSubstring which checks if one word is a substring
# of another. Given two strings, s1 and s2, write code to check if s2 is a rotation of s1 using only one
# call to isSubstring (e.g., "waterbottle" is a rotation of"erbottlewat").

def is_rotation(s1, s2):
    return len(s1) == len(s2) and s2 in s1 + s1


def __main():
    pass


if __name__ == '__main__':
    __main()
