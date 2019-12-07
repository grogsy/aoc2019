
class InvalidOpCode(BaseException):
    pass

class Computer:
    op_codes = {
        1, # add(a, b)
        2, # mul(a, b)
        3, # mov(a)
        4, # print(a)
        99 # exit
    }
    param_modes = {
        0, # indexed-position
        1  # as value
    }

    def __init__(self, instructions):
        self.instructions = instructions
        self.counter = 0

    def solution_one(self, noun = 12, verb = 1):
        data = self.instructions[:]
        data[1] = noun if noun else self.instructions[1]
        data[2] = verb if verb else self.instructions[2]

        i = 0
        while i < len(data): 
            op = data[i]
            params = None
            if op > 9 and op != 99:
                long = str(op)
                op = int(long[-2:])
                params = long[:-2]

            if op not in self.op_codes:
                i += 4
                continue
            elif op == 99:
                break

            x, y, pos = data[i + 1], data[i + 2], data[i + 3]

            if op == 1:
                x = x if params is not None and params[-1] == '1' else data[x]
                y = y if params is not None and len(params) > 1 and params[-2] == '1' else data[y]
                i += 4
                val = x + y
            elif op == 2:
                x = x if params is not None and params[-1] == '1' else data[x]
                y = y if params is not None and len(params) > 1 and params[-2] == '1' else data[y]
                i += 4
                val = x * y
            elif op == 3:
                val = int(input("Opcode 3, Diagnostic Input: "))
                i += 2
                pos = data[i + 1]
            elif op == 4:
                print("Diagnostic, value at data[{}]: {}".format(x, data[x]))
                i +=2
                continue

            data[pos] = val

        self.counter = 0
        return data[-1]

    def solution_two(self):
        for noun in range(100):
            for verb in range(100):
                try:
                    ans = self.solution_one(noun, verb)       
                except InvalidOpCode:
                    continue
                if ans == 19690720:
                    return 100 * noun + verb


if __name__=='__main__':
    instructions = list(map(int, open('2.txt').read().split(',')))

    intcode = Computer(instructions)

    print("Solution 1: ", intcode.solution_one())
    print("Solution 2: ", intcode.solution_two())