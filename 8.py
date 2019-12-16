with open('8.txt', 'r') as f:
    data = [int(digit) for digit in f.read()]

def get_layers(input, width=25, height=6):
    layer_size = width * height
    layers = [input[i: i + layer_size] for i in range(0, len(input), layer_size)]

    return layers

def check_encoding(data):
    smallest = min(data, key=lambda layer: layer.count(0))

    return smallest.count(1) * smallest.count(2)

def get_message(data):
    bits = []
    topmost_layer = data[0]
    for i in range(len(topmost_layer)):
        for j in range(len(data)):
            this_layer = data[j][i]
            if this_layer == 0 or this_layer == 1:
                bits.append(str(this_layer))
                break

    assert len(bits) == len(topmost_layer)
    output = [bits[i: i + 25] for i in range(0, len(bits), 25)]
    return output

from pprint import pprint
layers = get_layers(data)
print("Solution 1: {}".format(check_encoding(layers)))
output = get_message(layers)
for layer in output:
    print(layer)