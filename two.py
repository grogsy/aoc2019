
class InvalidOpCode(BaseException):
    pass

class Computer:
    op_codes = {
        1, # add(a, b)
        2, # mul(a, b)
        3, # mov(a)
        4, # print(a)
        5, # jt(a, b)
        6, # jf(a, b)
        7, # lt(a, b)
        8, # eq(a, b)
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

        while self.counter < len(data): 
            op = data[self.counter]
            params = None
            if op > 9 and op != 99:
                long = str(op)
                op = int(long[-2:])
                params = long[:-2]

            if op not in self.op_codes:
                self.counter += 4
                continue
            elif op == 99:
                break
            elif op == 3:
                val = int(input("Opcode 3, Diagnostic Input: "))
                self.counter += 2
                pos = data[self.counter + 1]
                data[pos] = val
                continue
            elif op == 4:
                x = data[self.counter + 1]
                print("Diagnostic, value at data[{}]: {}".format(x, data[x]))
                self.counter +=2
                continue
            
            x, y, pos = data[self.counter + 1], data[self.counter + 2], data[self.counter + 3]
            x = x if params is not None and params[-1] == '1' else data[x]
            y = y if params is not None and len(params) > 1 and params[-2] == '1' else data[y]

            if op == 1:
                self.counter += 4
                val = x + y
            elif op == 2:
                self.counter += 4
                val = x * y
            elif op == 5:
                self.counter = y if x else self.counter + 3
                continue
            elif op == 6:
                self.counter = y if x == 0 else self.counter + 3
                continue
            elif op == 7:
                val = 1 if x < y else 0
                self.counter += 4
            elif op == 8:
                val = 1 if x == y else 0
                self.counter += 4

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