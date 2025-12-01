dial_size = 100


def rotate_dial(current_position, command):
    direction, increment = command[0], int(command[1:])
    if direction == "L":
        return (current_position - increment) % dial_size
    else:
        return (current_position + increment) % dial_size


rotation_input = []
with open("./a_input.txt", "r") as file:
    for line in file:
        rotation_input.append(line.strip())

number_of_zeros = 0
next_position = 50
for rotation in rotation_input:
    next_position = rotate_dial(next_position, rotation)
    if next_position == 0:
        number_of_zeros += 1

print(number_of_zeros)
