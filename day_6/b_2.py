def get_input():
    lines = []
    with open("./test.txt", "r") as file:
        for line in file:
            lines.append([x for x in line])
    ops = [x for x in lines.pop(-1) if x != " "]
    return lines, ops


input, ops = get_input()

transposed = ["".join(list(row)).strip() for row in zip(*input)]

rows = []
row = []
for item in transposed:
    if item != "":
        row.append(item)
    else:
        rows.append(row)
        row = []


def mather(arg1, arg2, op):
    if op == "*":
        return int(arg1) * int(arg2)
    if op == "+":
        return int(arg1) + int(arg2)


sum = 0
for ir, row in enumerate(rows):
    answer = row[0]
    for item in row[1:]:
        answer = mather(answer, item, ops[ir])
    sum += answer


print(sum)
