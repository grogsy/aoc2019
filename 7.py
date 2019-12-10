from itertools import permutations
from intcode import AmplifierController

with open('7.txt', 'r') as data:
    instructions = list(map(int, data.read().split(',')))

def solution_one():
    max_signal = 0
    for setting in permutations(range(5), 5):
        amplifiers = [AmplifierController(phase_setting, instructions=instructions, silent=True) for phase_setting in setting]
        next_input_signal = 0
        for a in amplifiers:
            a.input_signal = next_input_signal
            a.parse_instructions()
            next_input_signal = a.input_signal

        if a.input_signal > max_signal:
            max_signal = a.input_signal

    print("SOLUTION ONE:")
    print(max_signal)

def solution_two():
    max_signal = 0
    for setting in permutations(range(10), 5):
        amplifiers = [AmplifierController(phase_setting, instructions=instructions, silent=True) for phase_setting in setting]

        next_input_signal = 0
        for a in amplifiers:
            a.input_signal = next_input_signal
            a.parse_instructions()
            next_input_signal = a.input_signal

        amp_tracker = 0
        prev_amp = a
        current_amp = amplifiers[amp_tracker]
        current_amp.input_signal = a.input_signal

        while True:
            current_amp.parse_instructions()
            if current_amp.halt:
                break
            prev_amp = current_amp
            next_input_signal = prev_amp.input_signal
            amp_tracker += 1
            if amp_tracker >= len(amplifiers):
                amp_tracker = 0
            current_amp = amplifiers[amp_tracker]
            current_amp.input_signal = next_input_signal

        if amplifiers[-1].input_signal > max_signal:
            max_signal = amplifiers[-1].input_signal

    print("SOLUTION TWO")
    print(max_signal)

solution_one()
solution_two()