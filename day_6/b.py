ops = None


def get_input():
    lines = []
    ops = None
    with open("./input.txt", "r") as file:
        for line in file:
            lines.append([[x, c] for x, c in enumerate(line)])
            ops = line
    ops = [x for x in ops.strip().split(" ") if x != ""]
    return lines, ops


input, ops = get_input()

input.pop(-1)

input_grouped = []
for xr, row in enumerate(input):
    input_grouped.append([])
    number_set = []
    for x in row:
        if x[1] == " " and len(number_set) == 0:
            continue
        elif x[1] == " " or x[1] == "\n":
            input_grouped[xr].append(number_set)
            number_set = []
        else:
            number_set.append(x)
    if len(number_set) > 0:
        input_grouped[xr].append(number_set)


transposed = [list(row) for row in zip(*input_grouped)]

ordered = []
for xr, row in enumerate(transposed):
    min_char_x = None
    max_char_x = None
    for item in row:
        for digit in item:
            if min_char_x == None or digit[0] < min_char_x:
                min_char_x = digit[0]
            if max_char_x == None or digit[0] > max_char_x:
                max_char_x = digit[0]
    numbers = [""] * (max_char_x - min_char_x + 1)
    for item in row:
        for digit in item:
            numbers[digit[0] - min_char_x] += str(digit[1])

    ordered.append(numbers)


def mather(arg1, arg2, op):
    if op == "*":
        return int(arg1) * int(arg2)
    if op == "+":
        return int(arg1) + int(arg2)


answers = []
for xr, row in enumerate(ordered):
    op = ops[xr]
    answer = int(row[0])
    print(row, answer)
    for x in row[1:]:
        answer = mather(answer, x, op)
    answers.append(answer)

print(answers)
print(sum(answers))
