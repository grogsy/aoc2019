from itertools import permutations
from two import Computer

with open('7.txt', 'r') as data:
    instructions = list(map(int, data.read().split(',')))

def test_amplifiers(instructions, settings):

    phase_setting, input_signal = [settings[0], 0]

    intcode = Computer(instructions, amp_settings=[phase_setting, input_signal])
    output = intcode.parse_instructions()

    for setting in settings[1:]:
        intcode = Computer(instructions, amp_settings=[setting, output])
        output = intcode.parse_instructions()

    return output



print(max([test_amplifiers(instructions, setting) for setting in permutations(range(5), 5)]))