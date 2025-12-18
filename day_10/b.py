from scipy.optimize import linprog


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


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


input = get_input()
# i do feel guilty using scipy but the other way took wayyyy too long
total = 0
for config in input:
    # just get the sum func
    obj_func = [1] * len(config[1])
    A = config[1]
    out = config[2]
    results = linprog(
        c=obj_func, A_eq=transpose(A), b_eq=out, method="highs", integrality=True
    )
    total += results.fun
print(total)
# transposed = [list(row) for row in zip(*input_grouped)]

print(config)
