import random
from typing import Tuple

def randint(min: int, max: int) -> int:
    """
    Return random integer in range `[min, max)`.
    """
    return random.randint(min, max - 1)

def randfloat(min: float, max: float) -> float:
    """
    Return random float in range `[min, max)`.
    """
    return min + (max - min) * random.random()

def clamp(min_val: float, x: float, max_val: float) -> float:
    return max(min_val, min(max_val, x))

def rand_vertex(lims: Tuple[int, int]):
    return (randint(0, lims[0]), randint(0, lims[1]))

def sum_vec(v1: Tuple[int, int], v2: Tuple[int, int]):
    return (v1[0] + v2[0], v1[1] + v2[1])
