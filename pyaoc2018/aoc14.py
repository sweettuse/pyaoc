__author__ = 'acushner'

NUM_RECIPES = 430971


def create(num_recipes=NUM_RECIPES, return_num_before=False):
    recipes = [3, 7]
    e1, e2 = 0, 1
    new_idx = lambda idx: (idx + recipes[idx] + 1) % len(recipes)

    def _update():
        while True:
            nonlocal e1, e2
            new_recipe = recipes[e1] + recipes[e2]

            if new_recipe >= 10:
                recipes.append(1)
                yield
            recipes.append(new_recipe % 10)
            yield

            e1 = new_idx(e1)
            e2 = new_idx(e2)

    u = _update()
    if return_num_before:
        match = list(map(int, str(num_recipes)))
        while recipes[-len(match):] != match:
            next(u)
        return len(recipes) - len(match)

    else:
        while len(recipes) < num_recipes + 10:
            next(u)
        return recipes[num_recipes:num_recipes + 10]


def part1():
    return ''.join(map(str, create()))


def part2():
    return create(return_num_before=True)


def __main():
    print(part1())
    print(part2())


if __name__ == '__main__':
    __main()
