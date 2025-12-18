import itertools
import math


def vec_add(x, y):
    # x = [1] y = [2,3]
    output_size = max(len(x), len(y))
    output = [0 for x in range(output_size)]
    for i in range(output_size):
        output[i] = (x[i] if i < len(x) else 0) + (y[i] if i < len(y) else 0)
    return output


def parse_light_diagram(text):
    # '[.##.]'
    diagram = text[1:-1]
    diagram = [1 if x == "#" else 0 for x in diagram]
    return diagram


def parse_schematics(schematics_str_list, length):
    schematics = [x[1:-1].split(",") for x in schematics_str_list]
    max_len = length
    parsed = []
    for schematic in schematics:
        empty = [0 for _ in range(max_len)]
        for x in schematic:
            empty[int(x)] = 1
        parsed.append(empty)

    return parsed


def parse_joltage(text):
    joltage = text[1:-1].split(",")
    return [int(x) for x in joltage]


def get_input():
    with open("./input.txt", "r") as file:
        rows = []
        for line in file:
            row = line.strip().split(" ")
            light_diagram = parse_light_diagram(row[0])
            schematics = parse_schematics(row[1:-1], len(light_diagram))
            joltage = parse_joltage(row[-1])
            rows.append([light_diagram, schematics, joltage])
        return rows


input = get_input()

# time to write a gaussian solver

# [.##.] x(3) y(1,3) z(2) a(2,3) b(0,2) c(0,1)
# x 0,0,0,1
# y 0,1,0,1
# z 0,0,1,0
# a 0,0,1,1
# b 1,0,1,0
# c 1,1,0,0

#   0,1,1,0

# are there any buttons


def solver(steps, solution):
    out = [0] * len(steps[0])
    for step in steps:
        for x in range(len(step)):
            out[x] += step[x]
    out = [x % 2 for x in out]
    return out == solution


def get_solution(config):
    number_of_combinations = 0
    found_solution = False
    while not found_solution:
        number_of_combinations += 1
        combos = itertools.combinations_with_replacement(
            config[1], number_of_combinations
        )
        for combo in combos:
            if solver(combo, config[0]):
                print(combo, len(combo))
                return len(combo)


total = 0
for config in input:
    total += get_solution(config)

print(total)
exit()
print("----------")


def sort_rows(matrix, column):
    before_column = matrix[0:column]
    after_column = matrix[column:]
    after_column.sort(key=lambda x: x[0][column], reverse=True)
    return before_column + after_column


def gaussian_elimination(equation):
    result = equation[0]
    button_configs = equation[1]
    matrix = []
    for x in range(len(result)):
        row = []
        for y in button_configs:
            row.append(y[x])
        matrix.append([row, result[x]])

    matrix = sort_rows(matrix, 0)

    print(matrix)
    for x in range(len(matrix) - 1):
        matrix = sort_rows(matrix, x + 1)
        print(matrix)


gaussian_elimination(input[0])
