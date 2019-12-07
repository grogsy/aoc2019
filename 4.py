check = range(153517, 630396)

def has_double(num) -> int:
    num = list(map(int, str(num)))
    return any(num[i] == num[i + 1] for i in range(len(num) - 1))

def increasing(num) -> int:
    num = list(map(int, str(num)))
    return all(num[i] <= num[i + 1] for i in range(len(num) - 1))


print(len([num for num in check if has_double(num) and increasing(num)]))