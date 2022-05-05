from typing import List
import numpy as np
# TODO: design heuristic function to support owned positions


def l1(v1: List[int], v2: List[int], n) -> int:
    """ computes L1 distance between v1 and v2 - L1 modified for the hexagonal grid """
    if type(v1) == type(v2) == str: return n
    if type(v1) != type(v2) and (type(v1) == str or type(v2) == str): return 1

    print(v1, v2)
    x0, y0 = v1[0], v1[1],
    x1, y1 = v2[0], v2[1]
    dx = x1 - x0
    dy = y1 - y0
    if np.sign(dx) == np.sign(dy):
        distance = abs(dx + dy)
    else:
        distance = max(abs(dx), abs(dy))
    return distance
