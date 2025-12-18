import itertools


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


def count_paths_between(graph, start, end, memo):
    if start == end:
        return 1
    if start in memo:
        return memo[start]

    count = 0
    if start in graph:
        for neighbor in graph[start]:
            count += count_paths_between(graph, neighbor, end, memo)

    memo[start] = count
    return count


def count_paths_through_nodes(graph, source, destination, required_nodes):
    nodes_sequence = [source, *required_nodes, destination]

    total_paths = 1
    for u, v in itertools.pairwise(nodes_sequence):
        paths_segment = count_paths_between(graph, u, v, {})
        total_paths *= paths_segment

        if total_paths == 0:
            return 0

    return total_paths


source_node = "svr"
destination_node = "out"
# no paths from dac to fft so fft must be before dac
required_list = ["fft", "dac"]
print(input)
graph = {key: value for key, value in input}

paths = count_paths_through_nodes(graph, source_node, destination_node, required_list)
print(
    f"Number of paths from {source_node} to {destination_node} passing through {required_list}: {paths}"
)
