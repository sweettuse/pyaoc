__author__ = 'acushner'


# https://leetcode.com/problems/clone-graph/

class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


def _cache(node, nodes):
    if not node or node.val in nodes:
        return
    nodes[node.val] = (Node(node.val), node)
    for n in node.neighbors:
        _cache(n, nodes)


class Solution:
    def cloneGraph(self, node: 'Node') -> 'Node':
        if not node:
            return

        nodes = {}
        _cache(node, nodes)
        for new, orig in nodes.values():
            new.neighbors = [nodes[n.val][0] for n in orig.neighbors]
        return next(iter(nodes.values()))[0]


def __main():
    pass


if __name__ == '__main__':
    __main()
