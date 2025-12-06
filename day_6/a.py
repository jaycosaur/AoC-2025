def get_input():
    lines = []
    with open("./input.txt", "r") as file:
        for line in file:
            lines.append([x for x in line.strip().split(" ") if len(x) > 0])
    return lines


input = get_input()
ops = input.pop(-1)


def mather(arg1, arg2, op):
    if op == "*":
        return int(arg1) * int(arg2)
    if op == "+":
        return int(arg1) + int(arg2)


answers = input.pop(0)
for row in input:
    for x, op in enumerate(ops):
        answers[x] = mather(answers[x], row[x], op)

print(answers)
print(sum(answers))
