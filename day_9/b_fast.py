from itertools import combinations


def get_input():
    with open("./input.txt", "r") as file:
        rows = []
        for line in file:
            rows.append([int(x) for x in line.strip().split(",")])
        return rows


input = get_input()


# [1,4] [2,7]
def ranges_overlap(range1, range2):
    r11, r12 = range1
    r21, r22 = range2

    # [1,2] [0,2]
    if r11 >= r21 and r11 <= r22:
        return True

    # [0,2] [1,3]
    if r12 >= r21 and r12 <= r22:
        return True

    # [0,4] [1,2]
    if r21 >= r11 and r21 <= r12:
        return True

    if r22 >= r11 and r22 <= r12:
        return True

    return False


class Cell:
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.connected_cells = set()

    def __repr__(self):
        return f"Cell({self.x},{self.y})"

    def __eq__(self, other):
        if not isinstance(other, Cell):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(str([self.x, self.y]))

    def connect_to(self, *cells):
        self.connected_cells.update(cells)

    def connections_intersect(self, cell_top_left, cell_bottom_right):
        # enclosed by the area so must intersect
        if (
            self.x >= cell_top_left.x
            and self.y >= cell_top_left.y
            and self.x <= cell_bottom_right.x
            and self.y <= cell_bottom_right.y
        ):
            return True

        x_line_cells = [self] + [c for c in list(self.connected_cells) if c.y == self.y]
        y_line_cells = [self] + [c for c in list(self.connected_cells) if c.x == self.x]

        min_x, max_x = min([c.x for c in x_line_cells]), max(
            [c.x for c in x_line_cells]
        )
        min_y, max_y = min([c.y for c in y_line_cells]), max(
            [c.y for c in y_line_cells]
        )

        # if an x line it needs to be between the x bounds but can extend outside
        # AND it needs to be between the y bounds
        if self.y >= cell_top_left.y and self.y <= cell_bottom_right.y:
            if ranges_overlap([min_x, max_x], [cell_top_left.x, cell_bottom_right.x]):
                return True

        # if a y line it needs to be between the y bounds but can extend outside
        # AND it needs to be between the x bounds
        if self.x >= cell_top_left.x and self.x <= cell_bottom_right.x:
            if ranges_overlap([min_y, max_y], [cell_top_left.y, cell_bottom_right.y]):
                return True
        return False


input_cells = [Cell(pos) for pos in input]

# construct chains of cells that represent the borders of the areas
for cell in input_cells:
    cells_same_x_y = set(
        [
            compare_cell
            for compare_cell in input_cells
            if cell.y == compare_cell.y or cell.x == compare_cell.x
        ]
    )
    cells_same_x_y.remove(cell)
    cell.connect_to(*cells_same_x_y)


def calculate_area(cell_1: Cell, cell_2: Cell):
    area = (abs(cell_2.y - cell_1.y) + 1) * (abs(cell_2.x - cell_1.x) + 1)
    return area


cell_combinations = combinations(input_cells, 2)

areas = [[calculate_area(x1, x2), x1, x2] for x1, x2 in cell_combinations]
areas.sort(key=lambda x: x[0], reverse=True)

print("HERE")
for area, c1, c2 in areas:
    min_x, max_x = min(c1.x, c2.x), max(c1.x, c2.x)
    min_y, max_y = min(c1.y, c2.y), max(c1.y, c2.y)

    # construct cells that are 1 smaller
    cell_interior_top_left = Cell([min_x + 1, min_y + 1])
    cell_interior_bottom_right = Cell([max_x - 1, max_y - 1])

    has_intersection = False
    # loop over cells that are enclosed by c1,c2 and check if lines intersect
    for cell in input_cells:
        is_intersecting = cell.connections_intersect(
            cell_interior_top_left, cell_interior_bottom_right
        )
        if is_intersecting:
            has_intersection = is_intersecting
            break

    if not has_intersection:
        print(area, c1, c2)
        break
