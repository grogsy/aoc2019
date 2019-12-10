
class InvalidOpCode(BaseException):
    pass


class Computer:
    op_codes = {
        1,  # add(a, b)
        2,  # mul(a, b)
        3,  # mov(a)
        4,  # out(a)
        5,  # je(a, b)  jump equal to 0
        6,  # jne(a, b) jump not equal to 0
        7,  # lt(a, b)
        8,  # eq(a, b)
        99  # exit
    }

    def __init__(self, instructions):
        self.instructions = instructions
        self.counter = 0

        # subclasses will handle pause mechanism somehow
        self.paused = False

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
                self.handle_close()
                break
            elif op in (3, 4):
                self.handle_io(op)
                if self.paused:
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

    def handle_close(self):
        pass

    def handle_io(self, operation):
        if operation == 3:
            self.handle_input()
        if operation == 4:
            self.handle_output()

    def handle_input(self):
        raise NotImplementedError

    def handle_output(self):
        raise NotImplementedError


    def jcmp(self, operation, a, b):
        '''
        Jump compare
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

class DiagnosticTest(Computer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def handle_input(self):
        val = int(input("Opcode 3, Diagnostic Input: "))

        pos = self.working_set[self.counter + 1]
        self.working_set[pos] = val
        self.counter += 2
    
    def handle_output(self):
        address = self.working_set[self.counter + 1]
        print("Diagnostic Test, value at address {}: {}".format(address, self.working_set[address]))
        self.counter += 2

class AmplifierController(Computer):
    def __init__(self, phase_setting, silent=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_signal  = 0
        self.input_tracker = 0
        self.phase_setting = phase_setting

        self.silent = silent
        self.halt = False
        self.prev_counter = 0

    def parse_instructions(self):
        self.counter = self.prev_counter
        self.paused = False
        super().parse_instructions()

    def handle_close(self):
        self.halt = True

    def handle_input(self):
        if self.input_tracker == 0:
            # get input from phase_setting
            val = self.phase_setting
            self.input_tracker += 1
        else:
            # get input from input signal
            val = self.input_signal
        
        address = self.working_set[self.counter + 1]
        self.working_set[address] = val
        self.counter += 2

    def handle_output(self):
        address = self.working_set[self.counter + 1]
        self.input_signal = self.working_set[address]
        self.counter += 2
        if not self.silent:
            print(self.input_signal)

        # save working state
        self.instructions = self.working_set
        self.prev_counter = self.counter

        # lock amp from processing
        self.paused = True

