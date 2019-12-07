def orbit_count(data, count=0, parent='COM'):
    edges = 0 + count
    descendants = []

    for line in data:
        if line.startswith(parent + ')'):
            orbiter = line.split(')')[1]
            descendants.append(orbiter)

    depth = edges + 1
    for d in descendants:
        edges += orbit_count(data, count=depth, parent=d)

    return edges

def min_dist(data):
    start = [line for line in data if line.endswith(')YOU')][0]
    visited = {'YOU'}
    current_node = start.split(')')[0]
    return _min_dist(data, current=current_node, visited=visited)

def _min_dist(data, count=0, current=None, visited={}):
    visited.add(current)

    parents = [line.split(')')[0] for line in data if line.endswith(')'+current)]
    children = [line.split(')')[1] for line in data if line.startswith(current+')')]
    possible_paths = parents + children

    shortest = None
    if 'SAN' in possible_paths:
        return count

    for c in possible_paths:
        if c in visited:
            continue
        possible_path = _min_dist(data, count=count+1, current=c, visited=visited)
        if possible_path is not None and (shortest is None or possible_path < shortest):
            shortest = possible_path

    return shortest

with open('6.txt', 'r') as data:
    graph = data.read().split('\n')
    # print(orbit_count(graph))
    print(min_dist(graph))