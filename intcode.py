
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
        9,  # move relative base
        99  # exit
    }

    param_modes = {
        0: 'position_mode',
        1: 'immediate_mode',
        2: 'relative_mode'
    }

    def __init__(self, instructions, extend = False):
        self.instructions = instructions
        if extend:
            # make extends memory an optional feature
            self.instructions += ([0] * 2048)
        self.counter = 0
        self.relative_base = 0

        # subclasses will handle pause mechanism somehow
        self.paused = False

    def parse_instructions(self):
        self.working_set = self.instructions[:] 

        while self.counter < len(self.working_set):
            # print(self.working_set[self.counter: self.counter+4])
            op = self.working_set[self.counter]
            if op == 99:
                self.handle_close()
                break
            
            op, params = self.parse_operation(str(op))

            x = self.working_set[self.counter + 1]
            x = self.parse_parameter_mode(x, params.get('x'))

            if op not in Computer.op_codes:
                self.handle_unrecognized_opcode(op)
                continue
            elif op in (3, 4, 9):
                self.handle_single_param(op, x)
                if self.paused:
                    break
                continue

            y = self.working_set[self.counter + 2]
            y = self.parse_parameter_mode(y, params.get('y'))

            pos = self.working_set[self.counter + 3]

            if op in (5, 6):
                self.jcmp(op, x, y)
            elif op in (1, 2, 7, 8):
                self.set_value_at_address(op, x, y, pos)
        
        self.counter = 0

    def parse_parameter_mode(self, value, param):
        if param == 'position_mode':
            value = self.working_set[value]
        elif param == 'relative_mode':
            value = self.working_set[self.relative_base + value]
        elif param != 'immediate_mode':
            raise ValueError('unrecognized param: {}'.format(param))

        return value

    def parse_operation(self, operation):
        op = int(operation[-2:])
        x = 0
        y = 0

        if len(operation) > 2:
            param_codes = operation[:-2]
            x = int(param_codes[-1])
            if len(param_codes) > 1:
                y = int(param_codes[-2])

        params = {
            'x': Computer.param_modes.get(x, 'position_mode'),
            'y': Computer.param_modes.get(y, 'position_mode')
        }

        return op, params

    def handle_unrecognized_opcode(self, operation):
        self.counter += 4

    def handle_close(self):
        pass

    def handle_single_param(self, operation, value):
        if operation == 9:
            self.relative_base += value
            self.counter += 2
        elif operation in (3, 4):
            self.handle_io(operation, value)
        else:
            print("unknown op {}".format(operation))

    def handle_io(self, operation, value):
        if operation == 3:
            self.handle_input(value)
        if operation == 4:
            self.handle_output(value)

    def handle_input(self, value):
        raise NotImplementedError

    def handle_output(self, value):
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

    def handle_input(self, value):
        val = int(input("Opcode 3, Diagnostic Input: "))

        # pos = self.working_set[self.counter + 1]
        self.working_set[value] = val
        self.counter += 2
    
    def handle_output(self, value):
        # address = self.working_set[self.counter + 1]
        # print("Diagnostic Test, value at address {}: {}".format(address, self.working_set[address]))
        print("Diagnostic Test Value: {}".format(value))
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

    def handle_input(self, _):
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

    def handle_output(self, value):
        # address = self.working_set[self.counter + 1]
        # self.input_signal = self.working_set[address]
        self.input_signal = value
        self.counter += 2
        if not self.silent:
            print(self.input_signal)

        # save working state
        self.instructions = self.working_set
        self.prev_counter = self.counter

        # lock amp from processing
        self.paused = True

