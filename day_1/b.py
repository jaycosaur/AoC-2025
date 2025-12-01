import math


dial_size = 100


def rotate_dial(current_position, command):
    direction, increment = command[0], int(command[1:])

    next_position = None
    if direction == "L":
        next_position = (current_position - increment) % dial_size
    else:
        next_position = (current_position + increment) % dial_size

    # minimum number of ticks if > dial size
    zero_ticks = math.floor(increment / dial_size)

    zero_ticks = 0
    if direction == "L":
        # finished on zero
        if increment > 0 and next_position == 0 and current_position != 0:
            zero_ticks += 1
        # must have gone over 0
        elif next_position > current_position and current_position != 0:
            zero_ticks += 1
        # more than a full loop
        if increment > dial_size:
            zero_ticks += math.floor(increment / dial_size)
    elif direction == "R":
        # finished on zero
        if increment > 0 and next_position == 0 and current_position != 0:
            zero_ticks += 1
        # must have gone over 0
        elif next_position < current_position:
            zero_ticks += 1
        # more than a full loop
        if increment > dial_size:
            zero_ticks += math.floor(increment / dial_size)

    return next_position, zero_ticks


# left is back
# R is forward

print(rotate_dial(1, "L201"))  # 0 | 3
print(rotate_dial(99, "R201"))  # 0 | 3 ----
print(rotate_dial(1, "R1"))  # 2 | 0
print(rotate_dial(99, "L1"))  # 98 | 0
print(rotate_dial(1, "L1"))  # 0 | 1
print(rotate_dial(1, "L101"))  # 0 | 2
print(rotate_dial(99, "R1"))  # 0 | 1 ----
print(rotate_dial(99, "R101"))  # 0 | 2 ----
print(rotate_dial(1, "L2"))  # 99 | 1
print(rotate_dial(99, "R2"))  # 1 | 1
print(rotate_dial(0, "L200"))  # 0 | 2
print(rotate_dial(0, "R200"))  # 0 | 2
print(rotate_dial(0, "L400"))  # 0 | 4
print(rotate_dial(0, "R400"))  # 0 | 4

print(rotate_dial(0, "L5"))  # 95 | 0

rotation_input = []
with open("./a_input.txt", "r") as file:
    for line in file:
        rotation_input.append(line.strip())

number_of_zeros = 0
next_position = 50
for rotation in rotation_input:
    next_position, skipped_zero_count = rotate_dial(next_position, rotation)
    number_of_zeros += skipped_zero_count

print(number_of_zeros)
