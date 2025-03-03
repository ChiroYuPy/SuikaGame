from src.math.constants import MOMENT_OF_INERTIA


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

def generate_combinations(elements):
    num_elements = len(elements)
    for i in range(num_elements - 1):
        for j in range(i + 1, num_elements):
            yield elements[i], elements[j]

def get_moment_of_inertia(shape, *params):
    if shape in MOMENT_OF_INERTIA:
        return MOMENT_OF_INERTIA[shape](*params)
    else:
        raise ValueError(f"Shape '{shape}' is not defined in the moment of inertia dictionary.")