
class InvalidOpCode(BaseException):
    pass


class Computer:

    op_codes = {
        1,  # add(a, b)
        2,  # mul(a, b)
        3,  # mov(a)
        4,  # out(a)
        5,  # je(a, b)
        6,  # jne(a, b)
        7,  # lt(a, b)
        8,  # eq(a, b)
        99  # exit
    }

    def __init__(self, instructions, test=False, amp_settings=None):
        self.instructions = instructions

        self.counter = 0
        self.testing = test

        self.amp_settings = amp_settings
        self.using_amplifier = True if amp_settings else False
        self.amplifier_output = None
        self.cached_amp_settings = amp_settings

    def parse_instructions(self):
        self.working_set = self.instructions[:]

        while self.counter < len(self.working_set):
            op = self.working_set[self.counter]
            params = {}
            if op > 9 and op != 99:
                param_op = str(op)
                op, params = self.parse_parameter_mode(param_op)

            if op not in Computer.op_codes:
                self.handle_unrecognized_opcode(op)
                continue
            elif op == 99:
                break
            elif op in (3, 4):
                self.handle_io(op)
                if self.amplifier_output:
                    break
                continue

            x, y, pos = self.working_set[self.counter + 1], self.working_set[self.counter + 2], self.working_set[self.counter + 3]

            if not params.get('x_immediate_mode'):
                x = self.working_set[x]
            if not params.get('y_immediate_mode'):
                y = self.working_set[y]

            if op in (5, 6):
                self.jcmp(op, x, y)
            elif op in (1, 2, 7, 8):
                self.set_value_at_address(op, x, y, pos)

        self.counter = 0

        if self.testing:
            return "Test Concluded"
        elif self.amplifier_output is not None:
            output = self.amplifier_output
        else:
            output = self.working_set
        return output

    def parse_parameter_mode(self, operation):
        op = int(operation[-2:])
        param_codes = operation[:-2]

        params = {
            'x_immediate_mode': True if param_codes[-1] == '1' else False,
            'y_immediate_mode': True if (len(param_codes) > 1 and param_codes[-2] == '1') else False,
        }

        return op, params

    def handle_unrecognized_opcode(self, operation):
        self.counter += 4

    def handle_io(self, operation):
        if operation == 3:
            self.handle_input()
        if operation == 4:
            self.handle_output()

        self.counter += 2

    def handle_input(self):
        if self.testing:
            val = int(input("Opcode 3, Diagnostic Input: "))
        elif self.amp_settings:
            val = self.amp_settings.pop(0)

        pos = self.working_set[self.counter + 1]
        self.working_set[pos] = val

    def handle_output(self):
        x = self.working_set[self.counter + 1]
        if self.testing:
            print("Diagnostic, value at self.working_set[{}]: {}".format(x, self.working_set[x]))
        elif self.using_amplifier:
            self.amplifier_output = self.working_set[x]

    def jcmp(self, operation, a, b):
        '''
        Jump compare
        Set instruction counter to b if condition applied to a evaluates to true,
        Otherwise do nothing(counter moves up based on params taken (operation + 2 params = 3 moves up))
        '''
        if operation == 5:
            self.counter = b if a != 0 else self.counter + 3
        elif operation == 6:
            self.counter = b if a == 0 else self.counter + 3

    def set_value_at_address(self, operation, a, b, pos):
        if operation == 1:
            val = a + b
        elif operation == 2:
            val = a * b
        elif operation == 7:
            val = 1 if a < b else 0
        elif operation == 8:
            val = 1 if a == b else 0

        self.working_set[pos] = val
        self.counter += 4


if __name__ == '__main__':
    instructions = list(map(int, open('2.txt').read().split(',')))

    intcode = Computer(instructions)

    intcode.instructions[1] = 12
    intcode.instructions[2] = 1
    print("Solution 1: ")
    print(intcode.parse_instructions()[0])
    print("Solution 2: ")
    for noun in range(100):
        for verb in range(100):
            try:
                intcode.instructions[1] = noun
                intcode.instructions[2] = verb
                ans = intcode.parse_instructions()[0]
            except:
                continue
            if ans == 19690720:
                print(100 * noun + verb)
