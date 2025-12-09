from itertools import combinations
from collections import deque


def get_input():
    with open("./input.txt", "r") as file:
        rows = []
        for line in file:
            rows.append([int(x) for x in line.strip().split(",")])
        return rows


input = get_input()

empty_cell = None
red = 1
green = 2


class Cell:
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def __repr__(self):
        return f"Cell({self.x},{self.y})"

    def __eq__(self, other):
        if not isinstance(other, Cell):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(str([self.x, self.y]))


def get_surronding_cells(cell, grid):
    neighbours = []
    if cell.x > 1:
        pos = [cell.x - 1, cell.y]
        if grid[pos[1]][pos[0]] == ".":
            neighbours.append(Cell(pos))
    if cell.x < len(grid[0]) - 1:
        pos = [cell.x + 1, cell.y]
        if grid[pos[1]][pos[0]] == ".":
            neighbours.append(Cell(pos))
    if cell.y > 1:
        pos = [cell.x, cell.y - 1]
        if grid[pos[1]][pos[0]] == ".":
            neighbours.append(Cell(pos))
    if cell.y < len(grid) - 1:
        pos = [cell.x, cell.y + 1]
        if grid[pos[1]][pos[0]] == ".":
            neighbours.append(Cell(pos))

    return neighbours


def search_for_edges(cell, grid):
    if grid[cell.y][cell.x] != ".":
        return [], False

    visited = set()
    queue = deque([cell])
    visited.add(cell)
    traversal_order = []

    while queue:
        current_cell = queue.popleft()
        traversal_order.append(current_cell)

        # explore neighbours
        neighbours = get_surronding_cells(current_cell, grid)
        for neighbour in neighbours:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)

    touched_side = False
    for cell in visited:
        if (
            cell.x == 0
            or cell.y == 0
            or cell.x == len(grid[0]) - 1
            or cell.y == len(grid) - 1
        ):
            touched_side = True

    return visited, touched_side


def grid_builder():
    max_x = max([x for x, _ in input])
    min_x = min([x for x, _ in input])
    max_y = max([y for _, y in input])
    min_y = min([y for _, y in input])
    print("Building grid", max_x, max_y, min_x, min_y)
    row = ["." for x in range(max_x + 1)]
    grid = []
    for y in range(max_y + 1):
        grid.append(row.copy())
        if y % 1000 == 0:
            print(f"{y}/{max_y + 1}...")

    print("Placing reds", max_x, max_y)
    # place red tiles
    for rx, ry in input:
        grid[ry][rx] = "#"

    print("Placing greens")
    # find green rows
    for rx, ry in input:
        tiles_same_y = [tile for tile in input if tile[1] == ry]
        tiles_same_x = [tile for tile in input if tile[0] == rx]

        tile_same_y_left = None
        tile_same_y_right = None

        for tile_same_y in tiles_same_y:
            if tile_same_y[0] < rx:
                if tile_same_y_left is None:
                    tile_same_y_left = tile_same_y
                elif tile_same_y[0] < tile_same_y_left[0]:
                    tile_same_y_left = tile_same_y
            elif tile_same_y[0] > rx:
                if tile_same_y_right is None:
                    tile_same_y_right = tile_same_y
                elif tile_same_y[0] > tile_same_y_right[0]:
                    tile_same_y_right = tile_same_y

        tile_same_x_up = None
        tile_same_x_down = None

        for tile_same_x in tiles_same_x:
            if tile_same_x[1] < ry:
                if tile_same_x_down is None:
                    tile_same_x_down = tile_same_x
                elif tile_same_x[1] < tile_same_x_down[1]:
                    tile_same_x_down = tile_same_x
            else:
                if tile_same_x_up is None:
                    tile_same_x_up = tile_same_x
                elif tile_same_x[1] > tile_same_x_up[1]:
                    tile_same_x_up = tile_same_x

        if tile_same_y_left is not None:
            for gx in range(tile_same_y_left[0], rx):
                if grid[ry][gx] == ".":
                    grid[ry][gx] = "X"

        if tile_same_x_up is not None:
            # draw green tiles up to
            for gy in range(ry, tile_same_x_up[1]):
                if grid[gy][rx] == ".":
                    grid[gy][rx] = "X"

    # fill in all spaces between # or X
    # only need to search top -> down and left -> right
    # search around all .'s in the grid, if a search hits the edge of the map then it is not a X else X
    # print("Filling greens")
    # already_searched = set()

    # searched, touched_edge = search_for_edges(Cell([0, 0]), grid)
    # for cell in searched:
    #     grid[cell.y][cell.x] = "S"
    # for y in range(len(grid)):
    #     for x in range(len(grid[0])):
    #         cell = Cell([x, y])
    #         if cell in already_searched:
    #             continue
    #         searched, touched_edge = search_for_edges(Cell([x, y]), grid)
    #         already_searched.update(searched)
    #         if not touched_edge:
    #             for cell in searched:
    #                 grid[cell.y][cell.x] = "S"

    # for row in grid:
    #     print(" ".join(row))

    return grid


grid = grid_builder()

combos = combinations(input, 2)


def calculate_area(pos_1, pos_2):
    x0, y0 = pos_1
    x1, y1 = pos_2

    area = (abs(y1 - y0) + 1) * (abs(x1 - x0) + 1)

    return area


areas = [[calculate_area(x1, x2), x1, x2] for x1, x2 in combos]


areas.sort(key=lambda x: x[0], reverse=True)
print("Searching boxes")
areas_searched = 0
for area, x1, x2 in areas:
    areas_searched += 1
    print("Areas searched", areas_searched)
    not_enclosed = False
    for x in range(min(x1[0], x2[0]) + 1, max(x1[0], x2[0])):
        if not_enclosed:
            break
        for y in range(min(x1[1], x2[1]) + 1, max(x1[1], x2[1])):
            grid_cell = grid[y][x]
            if grid_cell == "X":
                not_enclosed = True
                break

    if not not_enclosed:
        print(area, x1, x2)
        break
