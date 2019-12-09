from two import Computer

with open('7.txt', 'r') as data:
    instructions = list(map(int, data.read().split(',')))

def test_amplifiers(instructions, settings):
    digits = list(map(int, str(settings)))
    if any(digit > 4 for digit in digits):
        return 0
    if len(digits) < 5:
        for _ in range(5 - len(digits)):
            digits.insert(0, 0)
    
    if len(digits) != len(set(digits)):
        return 0

    phase_setting, input_signal = [digits[0], 0]

    intcode = Computer(instructions, amp_settings=[phase_setting, input_signal])
    output = intcode.parse_instructions()

    for setting in digits[1:]:
        intcode = Computer(instructions, amp_settings=[setting, output])
        output = intcode.parse_instructions()

    return output


print(max([test_amplifiers(instructions, setting) for setting in range(40001)]))