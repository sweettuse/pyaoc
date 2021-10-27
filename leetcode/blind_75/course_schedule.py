from collections import defaultdict
from typing import List

__author__ = 'acushner'


# https://leetcode.com/problems/course-schedule/


def has_cycle(prereq_courses):
    path = set()
    visited = set()

    def visit(vertex):
        if vertex in visited:
            return False
        visited.add(vertex)
        path.add(vertex)
        for neighbour in prereq_courses.get(vertex, ()):
            if neighbour in path or visit(neighbour):
                return True
        path.remove(vertex)
        return False

    return any(visit(p) for p in prereq_courses)


def _prereq_courses(prerequisites):
    prereq_courses = defaultdict(set)
    for c, p in prerequisites:
        prereq_courses[p].add(c)
    return prereq_courses


class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        prereq_courses = _prereq_courses(prerequisites)

        if has_cycle(prereq_courses):
            return False

        courses = set().union(prereq_courses, *prereq_courses.values())
        return len(courses) <= numCourses


def __main():
    print(Solution().canFinish(5, [[1, 4], [2, 4], [3, 1], [3, 2]]))


if __name__ == '__main__':
    __main()
