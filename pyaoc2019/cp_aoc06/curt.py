from treelib import Tree


def main():
    # Read input orbit file and construct a Tree
    orbits = parse_orbits_file()
    orbital_tree = build_orbital_tree(orbits)

    # Calculate Advent of Code answers
    sum_total_orbits = sum_orbits(orbital_tree)
    path_to_santa = get_path_to_santa(orbital_tree)

    # Display program output
    orbital_tree.show()
    print('Sum total orbits: ' + str(sum_total_orbits))
    print('Distance to Santa: ' + str(len(path_to_santa) - 1))
    print('Path to Santa: ' + str(path_to_santa))


''' This method iterates over each node in the tree and cumulatively adds their depths.
Is there a more efficient way to calculate the total number of orbits?'''


def sum_orbits(orbital_tree):
    sum_total_orbits = 0

    for node in orbital_tree.all_nodes():
        sum_total_orbits += orbital_tree.depth(node)

    return sum_total_orbits


''' This method works by iteratively moving closer to the tree's root until Santa is seen
on a sub tree branch. Then we take the path straight to him.'''


def get_path_to_santa(orbital_tree):
    current_node = orbital_tree.parent('YOU')
    traverasl_complete = False
    path_to_santa = []

    while not traverasl_complete:
        if orbital_tree.subtree(current_node.identifier).contains('SAN'):
            paths = orbital_tree.subtree(current_node.identifier).paths_to_leaves()
            for path in paths:
                if 'SAN' in path:
                    path_to_santa += path[:-1]

            traverasl_complete = True
        else:
            path_to_santa.append(current_node.identifier)
            current_node = orbital_tree.parent(current_node.identifier)

    return path_to_santa


##### Helper Methods #####

'''This method takes a list of 'A)B' orbital pairs and returns a tree structure.
While there is more than 1 subtree, we iterate over the subtrees and join them one by one.'''


def build_orbital_tree(orbital_sub_trees):
    while len(orbital_sub_trees) > 1:
        for comp_tree_1 in orbital_sub_trees:

            index = orbital_sub_trees.index(comp_tree_1)
            for comp_tree_2 in orbital_sub_trees[(index + 1):]:

                if comp_tree_1.root in comp_tree_2:
                    for child in comp_tree_1.children(comp_tree_1.root):
                        comp_tree_2.paste(comp_tree_1.root, comp_tree_1.subtree(child.identifier))

                    orbital_sub_trees.remove(comp_tree_1)
                    break

                elif comp_tree_2.root in comp_tree_1:
                    for child in comp_tree_2.children(comp_tree_2.root):
                        comp_tree_1.paste(comp_tree_2.root, comp_tree_2.subtree(child.identifier))

                    orbital_sub_trees.remove(comp_tree_2)

    orbital_tree = orbital_sub_trees[0]

    return orbital_tree


# Parse orbits file into a list of orbital trees
def parse_orbits_file():
    orbits = []

    with open('orbits.txt') as orbits_file:
        orbits = [convert_to_tree(line) for line in orbits_file]

    return orbits


# Converts an 'A)B' string into a Tree object
def convert_to_tree(line):
    center, orbital = line.strip().split(')')

    new_tree = Tree()
    new_tree.create_node(identifier=center)
    new_tree.create_node(identifier=orbital, parent=new_tree.get_node(center))

    return new_tree


if __name__ == '__main__':
    main()