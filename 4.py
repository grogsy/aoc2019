check = range(153517, 630396)

def has_double(num) -> int:
    num = list(map(int, str(num)))
    return any(num[i] == num[i + 1] for i in range(len(num) - 1))

def increasing(num) -> int:
    num = list(map(int, str(num)))
    return all(num[i] <= num[i + 1] for i in range(len(num) - 1))

def part_two(num):
    num = list(map(int, str(num)))
    memo = {d: 0 for d in num}
    for d in num:
        memo[d] += 1
    return any(memo.get(k) == 2 for k in memo)


count = 0

for i in check:
    if increasing(i):
        if has_double(i):
            if part_two(i):
                count += 1


print(count)