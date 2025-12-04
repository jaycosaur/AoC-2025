def get_input():
    lines = []
    with open("./input.txt", "r") as file:
        for line in file:
            lines.append(list(line.strip()))
    return lines


input = get_input()


def parse_input():
    total_accessed = 0
    while True:
        number_accessed = 0
        to_remove = []
        for rx, row in enumerate(input):
            for cx, column in enumerate(row):
                if column == "@":
                    row_range = range(max(rx - 1, 0), min(rx + 2, len(input)))
                    col_range = range(max(cx - 1, 0), min(cx + 2, len(row)))
                    number_paper = 0
                    for r in row_range:
                        for c in col_range:
                            if input[r][c] == "@":
                                number_paper += 1
                    if number_paper < 5:
                        number_accessed += 1
                        to_remove.append((rx, cx))
        total_accessed += number_accessed
        for item in to_remove:
            input[item[0]][item[1]] = "."
        if number_accessed == 0:
            break
    print(total_accessed)

    # look for rolls of paper than scan around


parse_input()
