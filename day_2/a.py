def get_input():
    with open("./input.txt", "r") as file:
        for line in file:
            return line.split(",")
    return input


def parse_inputs(item_range: str):
    first, last = item_range.split("-")

    invalid_ids = []

    for id in range(int(first), int(last)):
        len_id = len(str(id))
        if len_id % 2 != 0:
            # skip odd length numbers
            continue
        id_as_str = str(id)
        half = int(len_id / 2)
        part_1, part_2 = id_as_str[0:half], id_as_str[half:]
        if part_1 == part_2:
            invalid_ids.append(id)

    return invalid_ids


lines_to_parse = get_input()
bad_ids = [parse_inputs(x) for x in lines_to_parse]
flat = [item for sublist in bad_ids for item in sublist]
print(sum(flat))
