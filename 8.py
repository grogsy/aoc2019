with open('8.txt', 'r') as f:
    data = [int(digit) for digit in f.read()]

def check_encoding(input, width=25, height=6):
    layer_size = width * height
    layers = [input[i: i + layer_size] for i in range(0, len(input), layer_size)]

    smallest = min(layers, key=lambda layer: layer.count(0))

    return smallest.count(1) * smallest.count(2)


from pprint import pprint
pprint(check_encoding(data))