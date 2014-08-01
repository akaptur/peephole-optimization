def iffer(condition):
    if condition:
        return 3
    else:
        return 10

def looper():
    total = 0
    for i in range(10):
        total += i
    return total

def continuer():
    a = b = c = 0
    for n in range(100):
        if n % 2:
            if n % 4:
                a += 1
            continue
        else:
            b += 1
        c += 1

    return a, b, c
