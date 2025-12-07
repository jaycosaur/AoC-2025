def get_input():
    with open("./input.txt", "r") as file:
        rows = []
        for line in file:
            rows.append([*line.strip()])
        return rows


input = get_input()
first_row = input.pop(0)

start = first_row.index("S")


class Node:
    def __init__(self, value):
        self.value = value
        self.paths = 1
        self.children = []  # For a general tree

    def __eq__(self, other):
        return self.value == other.value


tree = Node(start)
levels = tree

last_level = [tree]
level = 0
levels = []
for row in input:
    next_level = []
    for node in last_level:
        if row[node.value] == "^":
            # check if already exists in tree
            left_exists = [x for x in next_level if x.value == node.value - 1]
            right_exists = [x for x in next_level if x.value == node.value + 1]
            beam_left = (
                Node(node.value - 1) if len(left_exists) == 0 else left_exists[0]
            )
            beam_right = (
                Node(node.value + 1) if len(right_exists) == 0 else right_exists[0]
            )
            node.children = [beam_left, beam_right]
            if not left_exists:
                next_level.append(beam_left)
            if not right_exists:
                next_level.append(beam_right)
        else:
            straight_exists = [x for x in next_level if x.value == node.value]
            if not straight_exists:
                beam_straight = Node(node.value)
                node.children = [beam_straight]
                next_level.append(beam_straight)
            else:
                node.children = [straight_exists[0]]
    levels.append(last_level)
    last_level = next_level
    level += 1

# start at the bottom and go UP
for level in levels[::-1]:
    for x in level:
        x.paths = sum([y.paths for y in x.children])


print(levels[0][0].paths)
exit()
