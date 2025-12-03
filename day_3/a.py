def get_input():
    with open("./input.txt", "r") as file:
        rows = []
        for line in file:
            rows.append(line)
        return rows


banks = get_input()


def get_largest_batteries(bank):
    bank_as_str = str(bank).strip()
    first_battery = (int(bank_as_str[0]), 0)
    for idx, battery in enumerate(bank_as_str):
        if battery is None:
            continue
        if int(battery) > first_battery[0] and idx < len(bank_as_str) - 1:
            first_battery = (int(battery), idx)
    second_battery = (int(bank_as_str[first_battery[1] + 1]), first_battery[1] + 1)
    for idx, battery in enumerate(bank_as_str):
        if battery is None or idx <= second_battery[1]:
            continue
        if int(battery) > second_battery[0]:
            second_battery = (int(battery), idx)

    return f"{first_battery[0]}{second_battery[0]}"


print(get_largest_batteries("811111111111119"))

voltags = [int(get_largest_batteries(x)) for x in banks]
print(sum(voltags))
