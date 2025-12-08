import math


def get_input():
    with open("./input.txt", "r") as file:
        rows = []
        for line in file:
            rows.append([int(x) for x in line.strip().split(",")])
        return rows


input = get_input()


def get_distance_between(j0, j1):
    return math.sqrt((j0[0] - j1[0]) ** 2 + (j0[1] - j1[1]) ** 2 + (j0[2] - j1[2]) ** 2)


class JunctionBox:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def to_array(self):
        return [self.x, self.y, self.z]

    def distance_to(self, another_junction_box):
        return get_distance_between(self.to_array(), another_junction_box.to_array())

    def __repr__(self):
        return f"({self.x},{self.y},{self.z})"


junction_boxes = [JunctionBox(x, y, z) for x, y, z in input]

from itertools import combinations

possible_connections = list(combinations(junction_boxes, 2))

possible_connections.sort(key=lambda x: x[0].distance_to(x[1]))


# circuits have junction boxes (with connections) and wires
class Circuit:
    def __init__(self):
        self.connections = []
        self.boxes = set()

    def wires(self):
        return len(self.connections)

    def count_boxes(self):
        return len(self.boxes)

    def has_box(self, box):
        return box in self.boxes

    def __repr__(self):
        return f"Circuit({self.count_boxes()},{self.wires()})"


all_circuits = set()


def total_wires():
    return sum([circuit.wires() for circuit in all_circuits])


# for connection in possible_connections[0:1000]:
for connection in possible_connections:
    if len(all_circuits) == 1 and list(all_circuits)[0].count_boxes() == len(
        junction_boxes
    ):
        print(list(all_circuits)[0].connections[-1])
        break

    found_existing = False

    connection_0_circuit = None
    connection_1_circuit = None
    # check if either end of the connection exists in existing circuits
    for circuit in all_circuits:
        if connection[0] in circuit.boxes:
            connection_0_circuit = circuit
        if connection[1] in circuit.boxes:
            connection_1_circuit = circuit

    if connection_0_circuit is None and connection_1_circuit is None:
        new_circuit = Circuit()
        new_circuit.boxes.add(connection[0])
        new_circuit.boxes.add(connection[1])
        new_circuit.connections.append(connection)
        all_circuits.add(new_circuit)
        continue

    if connection_0_circuit == connection_1_circuit:
        new_circuit.connections.append(connection)
        continue

    if connection_0_circuit is None:
        connection_1_circuit.boxes.add(connection[0])
        connection_1_circuit.boxes.add(connection[1])
        connection_1_circuit.connections.append(connection)
        continue

    if connection_1_circuit is None:
        connection_0_circuit.boxes.add(connection[0])
        connection_0_circuit.boxes.add(connection[1])
        connection_0_circuit.connections.append(connection)
        continue

    # handle final case where connection exists across multiple circuits
    # use first circuit
    all_circuits.remove(connection_1_circuit)
    connection_0_circuit.connections += connection_1_circuit.connections
    connection_0_circuit.connections += [connection]
    connection_0_circuit.boxes.update(connection_1_circuit.boxes)

print("===========")
list_circuits = list(all_circuits)
list_circuits.sort(key=lambda x: -x.count_boxes())
print(list_circuits[0:4])
