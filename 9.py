from intcode import SensorBooster

# data = '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'.split(',')
# data = '1102,34915192,34915192,7,4,7,99,0'.split(',')
# data = '104,1125899906842624,99'.split(',')
# instructions = [int(num) for num in data]
with open('9.txt', 'r') as data:
    instructions = [int(num) for num in data.read().split(',')]



intcode = SensorBooster(instructions)

intcode.parse_instructions()