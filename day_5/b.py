def get_input():
    ranges = []
    ingredients = []
    is_ingrediants = False
    with open("./input.txt", "r") as file:
        for line in file:
            if line.strip() == "":
                is_ingrediants = True
                continue
            if is_ingrediants:
                ingredients.append(int(line.strip()))
            else:
                ranges.append([int(x) for x in line.strip().split("-")])
    return ranges, ingredients


def compactor(ranges):
    good_ranges = []
    print(ranges)
    for rb, rt in ranges:
        if len(good_ranges) == 0:
            good_ranges.append([rb, rt])
            continue
        new_bottom = rb
        new_top = rt
        ids_to_pop = []
        for rdx, good_range in enumerate(good_ranges):
            print(good_range, new_bottom, new_top)
            should_pop = False
            # look for ranges where bottom is overlapping and extend
            if new_bottom >= good_range[0] and new_bottom <= good_range[1]:
                new_bottom = good_range[0]
                should_pop = True
            # look for ranges where top is in between and extend
            if new_top >= good_range[0] and new_top <= good_range[1]:
                new_top = good_range[1]
                should_pop = True
            # look for ranges which are completely overlapped
            if new_bottom <= good_range[0] and new_top >= good_range[0]:
                should_pop = True
            if should_pop:
                ids_to_pop.append(rdx)
        good_ranges = [
            item for ix, item in enumerate(good_ranges) if ix not in ids_to_pop
        ]
        good_ranges.append([new_bottom, new_top])

    return good_ranges


def do_b():
    ranges, _ = get_input()
    comp = compactor(ranges)

    total = 0
    print(comp)
    for range in comp:
        total += range[1] - range[0] + 1
    print(total)


do_b()
