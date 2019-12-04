op_codes = {1, 2, 99}

instructions = list(map(int, open('2.txt').read().split(',')))

def solution_one(instructions, noun = 12, verb = 1):
    data = instructions[:]
    data[1] = noun
    data[2] = verb

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

    return data[0]

# print(solution_one(instructions))
# print(instructions)

def solution_2(data):
    for noun in range(100):
        for verb in range(100):
            try:
                ans = solution_one(data, noun=noun, verb=verb)       
            except:
                break
            if ans == 19690720:
                return 100 * noun + verb

print(solution_2(instructions))