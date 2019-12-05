from queue import deque

path_one, path_two = [deque(directions.split(',')) for directions in open('3.txt').read().split('\n')]
# path_one = deque('R8,U5,L5,D3'.split(','))
# path_two = deque('U7,R6,D4,L4'.split(','))

xs = {'L': -1, 'R': 1}
ys = {'U': 1, 'D': -1}

class Point:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.visited = set()

    def move(self, direction, magnitude):
        if direction in xs:
            direction = xs[direction]
            for i in range(1, magnitude + 1):
                self.visited.add((self.x + (i * direction), self.y))
            self.x += magnitude * direction
        else:
            direction = ys[direction]
            for i in range(1, magnitude + 1):
                self.visited.add((self.x, self.y + (i * direction)))
            self.y += magnitude * direction

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

p1 = Point()
p2 = Point()
min_dist = None

while path_one and path_two:
    next_move_1 = path_one.popleft()
    next_move_2 = path_two.popleft()

    p1.move(direction = next_move_1[0], magnitude = int(next_move_1[1:]))
    p2.move(direction = next_move_2[0], magnitude = int(next_move_2[1:]))

remaining = path_one or path_two

if remaining is path_one:
    unfinished = p1
    finished   = p2
else:
    unfinished = p2
    finished   = p1

while remaining:
    next_move = remaining.popleft()
    unfinished.move(direction = next_move[0], magnitude = int(next_move[1:]))

print(min(abs(p[0]) + abs(p[1]) for p in unfinished.visited & finished.visited))