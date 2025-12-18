def get_input():
    with open("./input.txt", "r") as file:
        rows = []
        for line in file:
            line = line.strip()
            input, out = line.split(":")
            output = out.strip().split(" ")
            rows.append([input, output])
        return rows


input = get_input()


class Device:
    def __init__(self, id):
        self.device_id = id
        self.connected_devices = set()
        self.marked = False
        self.sum_paths = 0

    def __repr__(self):
        return f"Device({self.device_id})"

    def connect_to_device(self, device):
        self.connected_devices.add(device)

    def get_children(self):
        return list(self.connected_devices)

    def has_connections(self) -> bool:
        return len(self.connected_devices) > 0

    def get_sum_paths(self):
        return self.sum_paths

    def mark(self, good_path: bool):
        if self.marked:
            print("OH NO", self)
        self.marked = True
        sum_paths = 0
        if len(self.connected_devices) == 0 and good_path:
            sum_paths += 1
        for child in self.connected_devices:
            sum_paths += child.sum_paths
        self.sum_paths = sum_paths


devices = {}


def get_or_upsert_device(device_id: str):
    exists = devices.get(device_id)
    if exists:
        return exists

    device = Device(device_id)
    devices[device_id] = device
    return device


for device_id, output_ids in input:
    device = get_or_upsert_device(device_id)
    for output_id in output_ids:
        out_device = get_or_upsert_device(output_id)
        device.connect_to_device(out_device)


def get_all_paths(device):
    all_paths = []
    current_path = []

    dac_device = get_or_upsert_device("dac")
    fft_device = get_or_upsert_device("fft")

    def dfs(node):
        if not node:
            return

        # Add the current node's value to the path
        current_path.append(node)

        if not node.has_connections():
            # If it's a leaf, add a copy of the current_path to all_paths
            all_paths.append(list(current_path))
        elif node.marked:
            # if already traversed then skip
            all_paths.append(list(current_path))
        else:
            # Recurse for all children
            for child in node.get_children():
                dfs(child)

        # Backtrack: remove the current node when returning from recursion
        # This allows exploration of other paths

        # check IF node has dac and fft in the path
        # this means that every child path (if ends at out) is a valid path
        #
        # if it does than mark as true else false
        node_to_mark = current_path.pop()

        if not node_to_mark.marked:
            print(node_to_mark)
            if dac_device in [*current_path, node_to_mark] and fft_device in [
                *current_path,
                node_to_mark,
            ]:
                node_to_mark.mark(True)
                print("Good path", node_to_mark)
                # print("Good path", node_to_mark.get_sum_paths())
            else:
                node_to_mark.mark(False)

    dfs(device)
    return all_paths


# for every device if you can't get to fft dac or out then mark as dead
start_device = get_or_upsert_device("svr")

# svr to out via dac and fft
paths_from_svr_to_out = [l for l in get_all_paths(start_device) if l[-1] == "out"]

print(start_device.sum_paths)
