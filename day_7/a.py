def get_input():
    with open("./input.txt", "r") as file:
        rows = []
        for line in file:
            rows.append([*line.strip()])
        return rows


input = get_input()
first_row = input.pop(0)

start = first_row.index("S")

beams = set([start])

split = 0
for row in input:
    new_beams = set()
    for beam_index in beams:
        if row[beam_index] == "^":
            new_beams.add(beam_index - 1)
            new_beams.add(beam_index + 1)
            split += 1
        else:
            new_beams.add(beam_index)
    beams = new_beams

print(new_beams, split)
