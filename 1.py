from math import floor
from functools import reduce

def calc(num):
    return floor(num / 3) - 2

def get_n_fuel(num):
    out = calc(num)
    next_num = calc(out)
    while next_num > 0:
        out += next_num
        next_num = calc(next_num)

    return out

data = map(int, open('1.txt').readlines())
# print(sum(calc(num) for num in data))
print(sum(get_n_fuel(num) for num in data))

# print(reduce(lambda x, y: x + (floor(y / 3) - 2), map(int, open('1.txt').readlines()), 0))