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
    factor = 10
    length_divided = lims[0] // factor
    height_divided = lims[1] // factor
    x = randint(0, length_divided) * factor
    y = randint(0, height_divided) * factor
    return (round(clamp(0, x, lims[0])), round(clamp(0, y, lims[1])))

def sum_vec(v1: Tuple[int, int], v2: Tuple[int, int]):
    return (v1[0] + v2[0], v1[1] + v2[1])

def swap_in_arr(arr, idx1, idx2):
    aux = arr[idx1]
    arr[idx1] = arr[idx2]
    arr[idx2] = aux
