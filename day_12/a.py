def list_to_int(l):
    return [int(i) for i in l]


def print_grid(grid):
    for row in grid:
        print("".join(row))


def rotate_cw_90(grid):
    return [list(reversed(col)) for col in zip(*grid)]


def flip(grid):
    return grid[::-1]


def get_present_transforms(present):
    transforms = [present]

    # rotate 90
    transforms.append(rotate_cw_90(present))
    # rotate 180
    transforms.append(rotate_cw_90(rotate_cw_90(present)))
    # rotate 270
    transforms.append(rotate_cw_90(rotate_cw_90(rotate_cw_90(present))))

    for x in transforms.copy():
        transforms.append(flip(x))

    return transforms


def replace_row(row, find, replace):
    return [replace if find == i else i for i in row]


present_ids = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "a", "b"]
present_counter = 0


def shape_to_id(shape, id):
    for r, _ in enumerate(shape):
        for c, _ in enumerate(shape[0]):
            if shape[c][r] != ".":
                shape[c][r] = id
    return shape


class Present:
    def __init__(self, shape):
        global present_counter
        self.id = str(present_ids[present_counter])
        self.shape = shape_to_id(shape, self.id)
        present_counter += 1
        self.variants = 8

    def __repr__(self):
        return f"Present({self.id})"

    def get_transforms(self):
        return get_present_transforms(self.shape)

    def print_variant(self, variant):
        print_grid(self.get_variant(variant))

    def get_variant(self, variant_number):
        if variant_number > (self.variants - 1):
            return None

        return self.get_transforms()[variant_number]


def get_input():
    is_reading_regions = False
    regions = []
    presents = []
    present = []
    with open("./test.txt", "r") as file:
        for line in file:
            line_clean = line.strip()
            if len(line_clean) == 0:
                if len(present) > 0:
                    presents.append(Present(present))
                    present = []
                continue
            if "x" in line_clean:
                is_reading_regions = True
            if not is_reading_regions and ":" in line_clean:
                continue
            if not is_reading_regions:
                present.append(list(line_clean))
            if is_reading_regions:
                grid, present_allocations = line_clean.split(":")
                regions.append(
                    [
                        list_to_int(grid.split("x")),
                        list_to_int(present_allocations.strip().split(" ")),
                    ]
                )

        return presents, regions


presents, regions = get_input()


def make_empty_grid(x, y):
    row = ["." for _ in range(x)]
    grid = [row.copy() for _ in range(y)]
    return grid


def check_presents_in_grid(presents_and_locations, grid):
    for present, present_variant, position in presents_and_locations:
        present_shape = present.get_variant(present_variant)
        for iy, row in enumerate(present_shape):
            for ix, x in enumerate(row):
                if x == ".":
                    continue
                if grid[iy + position[1]][ix + position[0]] != ".":
                    # collision and fail
                    # print("FAIL")
                    # print(present, present_variant, ix, iy, position[1], position[1])
                    # print_grid(grid)
                    return False
                grid[iy + position[1]][ix + position[0]] = x

    # print("PASS")
    # print_grid(grid)

    return True


def reset_grid(grid):
    for ir in range(len(grid)):
        for ic in range(len(grid[0])):
            grid[ir][ic] = "."


def next_present_change(present, max_x, max_y):
    # if doesn't fit first iterate through variations
    if present[1] != present[0].variants - 1:
        present[1] += 1
        # print(present_to_place[0].print_variant(present_to_place[1]))
        return present

    x, y = present[2]
    if x < max_x:
        present[1] = 0
        present[2][0] += 1
        return present
    if y < max_y:
        present[1] = 0
        present[2][0] = 0
        present[2][1] += 1
        return present

    return None


def fit_present_to_region(presents, grid):
    # print(presents, grid)
    # for each region for every present

    # ideally don't place 'spaces' near a wall if it can be avoided
    # print_grid(grid)

    presents_to_place = [[presents[0], 0, [0, 0]]]  # , [presents[1], 2, [1, 1]]
    check_presents_in_grid([[presents[0], 0, [0, 0]], [presents[1], 2, [1, 1]]], grid)
    max_x = len(grid[0]) - 3
    max_y = len(grid) - 3

    while True:
        reset_grid(grid)
        found_valid_present = False
        # input("~~~")
        # print(presents_to_place)
        # get next present to place
        present_to_place = presents_to_place[-1]
        print(len(presents), len(presents_to_place), present_to_place)

        does_fit = check_presents_in_grid(presents_to_place, grid)
        if does_fit:
            if len(presents_to_place) < len(presents):
                # move on to next shape
                presents_to_place.append([presents[len(presents_to_place)], 0, [0, 0]])
                continue
            # completed!
            return True

        found_valid_present = False
        while not found_valid_present:
            present_to_place = presents_to_place[-1]
            updated_present = next_present_change(present_to_place, max_x, max_y)

            if updated_present is not None:
                presents_to_place[-1] = updated_present
                found_valid_present = True
                continue

            if len(presents_to_place) > 1:
                presents_to_place.pop(),
                print("BACKTRACKING", len(presents_to_place), presents_to_place[-1])
            else:
                break

        if found_valid_present:
            continue

        # then once variations complete move onto next x,y
        # exhausted all options so need to back track
        print("FAILURE")
        break

        # if all variants and positions completed and cannot find a fit then pop last and continue

    # if shape cannot be placed then back track and attempt the next config

    return False


for region in [regions[2]]:
    grid_config, present_count = region
    present_set = []
    for i, x in enumerate(present_count):
        if x > 0:
            present_set.extend([presents[i]] * x)
    grid = make_empty_grid(*grid_config)
    has_solution = fit_present_to_region(present_set, grid)
    print("Has solution", has_solution)
