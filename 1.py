from math import floor
from functools import reduce

def calc(num):
    return floor(num / 3) - 2

data = map(int, open('1.txt').readlines())
print(sum(calc(num) for num in data))

# print(reduce(lambda x, y: x + (floor(y / 3) - 2), map(int, open('1.txt').readlines()), 0))