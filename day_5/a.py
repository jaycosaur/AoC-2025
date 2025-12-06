def get_input():
    ranges = []
    ingredients = []
    is_ingrediants = False
    with open("./input.txt", "r") as file:
        for line in file:
            if line.strip() == "":
                print("BLANK")
                is_ingrediants = True
                continue
            if is_ingrediants:
                ingredients.append(int(line.strip()))
            else:
                ranges.append([int(x) for x in line.strip().split("-")])
    return ranges, ingredients


def do_a():
    ranges, ingredients = get_input()
    count_fresh = 0
    for ingredient in ingredients:
        for r1, r2 in ranges:
            if (ingredient >= r1) and (ingredient <= r2):
                print(ingredient, r1, r2, "fresh")
                count_fresh += 1
                break
    print(count_fresh)


do_a()
