from intcode import DiagnosticTest

instructions = list(map(int, open('5.txt').read().split(',')))
# instructions = list(map(int,'1002,4,3,4,33'.split(',')))

intcode = DiagnosticTest(instructions)

intcode.parse_instructions()

