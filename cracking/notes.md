# test questions

1.9 String Rotation: Assume you have a method `isSubstring` which checks if one word is a substring of another. Given
two strings, 51 and 52, write code to check if 52 is a rotation of 51 using only one call to i5Sub5tring (e.g., "
waterbottle" is a rotation of"erbottlewat").

# to revisit

### chapter 1

- 1.7 Rotate Matrix: Given an image represented by an NxN matrix, where each pixel in the image is 4 bytes, write a
  method to rotate the image by 90 degrees. Can you do this in place? Hints: #51, # 100

### chapter 2

- 2.8 Loop Detection: Given a circular linked list, implement an algorithm that returns the node at the beginning of the
  loop. DEFINITION Circular linked list: A (corrupt) linked list in which a node's next pointer points to an earlier
  node, so as to make a loop in the linked list.
    - EXAMPLE
        - Input: A -> B -> C -> D -> E -> C [the same C as earlier]
        - Output: C

  Hints: #50, #69, #83, #90

### chapter 4

- `__init__` - dfs, bfs, adj lists, top sort, paths
- 4.6 Successor: Write an algorithm to find the "next" node (i.e., in-order successor) of a given node in a binary
  search tree. You may assume that each node has a link to its parent. Hints: #79, #91
- 4.7 Build Order: You are given a list of projects and a list of dependencies (which is a list of pairs of projects,
  where the second project is dependent on the first project). All of a project's dependencies must be built before the
  project is. Find a build order that will allow the projects to be built. If there is no valid build order, return an
  error.
    - EXAMPLE
    - Input:
        - projects: a, b, c, d, e, f
        - dependencies: (a, d), (f, b), (b, d), (f, a), (d, c)
    - Output: f, e, a, b, d, c
    - Hints: #26, #47, #60, #85, #725, #133
- NOTE: for 4.8, try with parent as well
- 4.8 First Common Ancestor: Design an algorithm and write code to find the first common ancestor of two nodes in a
  binary tree. Avoid storing additional nodes in a data structure. NOTE: This is not necessarily a binary search tree.
  Hints: #10, #16, #28, #36, #46, #70, #80, #96

### chapter 5

- review set, get, clear, update bits (p. 114)

### chapter 8

- 8.12 Eight Queens: Write an algorithm to print all ways of arranging eight queens on an 8x8 chess board so that none
  of them share the same row, column, or diagonal. In this case, "diagonal" means all diagonals, not just the two that
  bisect the board
- 8.11 Coins: Given an infinite number of quarters (25 cents), dimes (10 cents), nickels (5 cents), and pennies (1 cent)
  , write code to calculate the number of ways of representing n cents. Hints: #300, #324, #343, #380, #394
- 8.6 Towers of Hanoi: In the classic problem of the Towers of Hanoi, you have 3 towers and N disks of different sizes
  which can slide onto any tower. The puzzle starts with disks sorted in ascending order of size from top to bottom (
  i.e., each disk sits on top of an even larger one). You have the following constraints:
    - (1) Only one disk can be moved at a time.
    - (2) A disk is slid off the top of one tower onto another tower.
    - (3) A disk cannot be placed on top of a smaller disk. Write a program to move the disks from the first tower to
      the last using stacks.

### chapter 9

- continue with design questions

### chapter 10

- re-read sorting algo digest (p. 146)

### chapter 16

- 16.1 Number Swapper: Write a function to swap a number in place (that is, without temporary variables). Hints: #492, #715, #736
- 16.17 Contiguous Sequence: You are given an array of integers (both positive and negative). Find the contiguous
  sequence with the largest sum. Return the sum. EXAMPLE input:2, -8, 3, -2, 4, -10 Output: 5 ( i. e • , { 3, -2, 4})
  Hints:#530, #552, #566, #593, #613
- 16.21 - sum_swap. make sure you get the function right. write the algebra

### chapter 17

- try 17.15 with trie!
- 17.6 - count of 2's - get back at this one /red

---

### leetcode

- max_profit_scheduler.py: https://leetcode.com/problems/maximum-profit-in-job-scheduling/