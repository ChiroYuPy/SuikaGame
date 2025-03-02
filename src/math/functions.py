def linear_progression(t):
    return t

def ease_in_out_progression(t):
    return t * t * (3 - 2 * t)

def fibonacci(n):
    if n <= 0:
        raise ValueError('n must be a positive integer')
    elif n == 1:
        return 1
    elif n == 2:
        return 1
    else:
        a, b = 1, 1
        for _ in range(3, n + 1):
            a, b = b, a + b
        return b
