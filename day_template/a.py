def get_input():
    with open("./test.txt", "r") as file:
        rows = []
        for line in file:
            rows.append(line)
        return rows
