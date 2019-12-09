from itertools import permutations
from intcode import AmplifierTest

with open('7.txt', 'r') as data:
    instructions = list(map(int, data.read().split(',')))


instructions = '3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0'.split(',')
instructions = list(map(int, instructions))
phase_settings = (4,3,2,1,0)

intcode = AmplifierTest(phase_settings, instructions=instructions)
intcode.test_amplifiers()

# print(max([test_amplifiers(instructions, setting) for setting in permutations(range(5), 5)]))
# print(max([test_amplifiers(instructions, setting, feedback=True) for setting in permutations(range(10), 5)]))