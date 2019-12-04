op_codes = {1, 2, 99}

data = list(map(int, open('2.txt').read().split(',')))
data[1] = 12
data[2] = 2

for i in range(0, len(data), 4):
    op = data[i]
    if op not in op_codes:
        raise "Prob"
    x, y, pos = data[i + 1], data[i + 2], data[i + 3]

    if op == 1:
        val = data[x] + data[y]
    elif op == 2:
        val = data[x] * data[y]
    elif op == 99:
        break

    data[pos] = val

print(data[0])