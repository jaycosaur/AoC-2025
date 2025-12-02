def get_input():
    with open("./input.txt", "r") as file:
        for line in file:
            return line.split(",")
    return input


def parse_inputs(item_range: str):
    first, last = item_range.split("-")

    invalid_ids = []

    for id in range(int(first), int(last)):
        # so need to check all substrings from 0:len(id)/2
        id_as_str = str(id)
        len_id = len(id_as_str)
        for sub_str_length in range(1, len_id):
            if len_id % sub_str_length == 0:
                # divisible so test
                sub_str = id_as_str[0:sub_str_length]
                if len(id_as_str.replace(sub_str, "")) == 0:
                    invalid_ids.append(id)
                    break

    return invalid_ids


lines_to_parse = get_input()
bad_ids = [parse_inputs(x) for x in lines_to_parse]
flat = [item for sublist in bad_ids for item in sublist]
print(sum(flat))
