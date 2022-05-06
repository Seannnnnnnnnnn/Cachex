from typing import List
import numpy as np
# TODO: design heuristic function to support owned positions
from agent.consts import infinity, neg_infinity

start_goal_nodes = [(neg_infinity, 0), (infinity, 0), (0, neg_infinity), (0, infinity)]


def l1(v1, v2, n) -> int:
    """ computes L1 distance between v1 and v2 - L1 modified for the hexagonal grid """
    if type(v1) == type(v2) == str: return n
    if type(v1) != type(v2) and (type(v1) == str or type(v2) == str): return 1

    if v1 in start_goal_nodes and v2 in start_goal_nodes: return n
    if v1 in start_goal_nodes or v2 in start_goal_nodes: return 1

    x0, y0 = v1[0], v1[1],
    x1, y1 = v2[0], v2[1]

    dx = x1 - x0
    dy = y1 - y0
    if np.sign(dx) == np.sign(dy):
        distance = abs(dx + dy)
    else:
        distance = max(abs(dx), abs(dy))
    return distance


