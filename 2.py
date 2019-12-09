from intcode import Computer

instructions = list(map(int, open('2.txt').read().split(',')))

intcode = Computer(instructions)

intcode.instructions[1] = 12
intcode.instructions[2] = 1
print("Solution 1: ")
intcode.parse_instructions()
print(intcode.working_set[0])
print("Solution 2: ")
for noun in range(100):
    for verb in range(100):
        try:
            intcode.instructions[1] = noun
            intcode.instructions[2] = verb
            intcode.parse_instructions()
            ans = intcode.working_set[0]
        except:
            continue
        if ans == 19690720:
            print(100 * noun + verb)