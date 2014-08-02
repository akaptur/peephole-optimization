def iffer(condition):
    if condition:
        return 3
    else:
        return 10

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
