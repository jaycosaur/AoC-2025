def get_input():
    with open("./input.txt", "r") as file:
        rows = []
        for line in file:
            rows.append(line)
        return rows


banks = get_input()


def get_largest_batteries(bank):
    bank_as_str = str(bank).strip()
    number_of_batteries = 12
    batteries = []
    print(bank_as_str)
    for battery_idx in range(0, number_of_batteries):
        if battery_idx == 0:
            default = (int(bank_as_str[0]), 0)
            batteries.append(default)
        else:
            previous = batteries[battery_idx - 1]
            default = (int(bank_as_str[previous[1] + 1]), previous[1] + 1)
            batteries.append(default)

        # scan for largest stopping with a gap
        for cell_idx in range(
            default[1], len(bank_as_str) - (number_of_batteries - battery_idx) + 1
        ):
            value = bank_as_str[cell_idx]
            if int(value) > batteries[battery_idx][0]:
                batteries[battery_idx] = (int(value), cell_idx)
    print(batteries)
    return "".join([str(x[0]) for x in batteries])


voltags = [int(get_largest_batteries(x)) for x in banks]
print(sum(voltags))
