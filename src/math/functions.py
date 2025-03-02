import math


def linear_progression(t):
    return t

def ease_in_out(t):
    return t * t * (3 - 2 * t)

def exponential(t):
    return t * t

def logarithmic(t):
    return math.log1p(t * 9) / math.log(10)