import pprint

# def count_orbits(data):
#     counter = {}
#     for line in data:
#         orbitee, orbiter = line.split(")")
#         orbit_count = counter.get(orbitee)
#         if orbit_count is None:
#             counter[orbitee] = 0
#         counter[orbiter] = 1 + counter.get(orbitee)

#     pprint.pprint([item for item in counter if counter[item] == 0])
#     return sum(counter.values())

def orbit_count(data, count=0, parent='COM'):
    edges = 0 + count
    print(edges)
    descendants = []

    for line in data:
        if line.startswith(parent + ')'):
            orbiter = line.split(')')[1]
            descendants.append(orbiter)

    depth = edges + 1
    for d in descendants:
        edges += orbit_count(data, count=depth, parent=d)

    return edges

with open('6.txt', 'r') as data:
    graph = data.read().split('\n')
    print(orbit_count(graph))