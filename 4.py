check = range(153517, 630396)

def increasing(num) -> int:
    return all(num[i] <= num[i + 1] for i in range(len(num) - 1))

def has_double(num):
    memo = {d: 0 for d in num}
    for d in num:
        memo[d] += 1
    return any(memo.get(k) == 2 for k in memo)

def possible_pass(num):
    digits = list(map(int, str(num)))

    return increasing(digits) and has_double(digits)

count = 0

for i in check:
    if possible_pass(i):
        count += 1


print(count)