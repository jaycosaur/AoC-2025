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
    area = 0
    for r, _ in enumerate(shape):
        for c, _ in enumerate(shape[0]):
            if shape[c][r] != ".":
                shape[c][r] = id
                area += 1
    return shape, area


class Present:
    def __init__(self, shape):
        global present_counter
        self.id = str(present_ids[present_counter])
        id_shape, area = shape_to_id(shape, self.id)
        self.shape = id_shape
        present_counter += 1
        self.variants = 8
        self.area = area

    def __repr__(self):
        return f"Present({self.id, self.area})"

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
    with open("./input.txt", "r") as file:
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

number_found = 0
for region in regions:
    size, present_counts = region
    area = size[0] * size[1]

    total_pres_area = sum(
        [present_counts[x] * presents[x].area for x in range(len(present_counts))]
    )
    # hack for now without moving and rotating to filter down the list
    # check for if there is a enough space at all
    if total_pres_area < area:
        number_found += 1
    print(total_pres_area, area)

print(number_found)
