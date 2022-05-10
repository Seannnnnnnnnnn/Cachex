"""
Contains code for the distance heuristic used within A* search algorithm. As we have self-occupied spaces that we
can pass through with cost 0 - we update the distance function to subtract the cost of these potential distances
nodes along our path.
"""


import numpy as np
from collections import defaultdict
from random_group3.consts import infinity, neg_infinity

start_goal_nodes = [(neg_infinity, 0), (infinity, 0), (0, neg_infinity), (0, infinity)]


def r_q_dictionary(positions):
    rq_dictionary = defaultdict(int)
    for position in positions:
        r, q = position[0], position[1]
        rq_dictionary[r] += 1
        rq_dictionary[q] += 1
    return rq_dictionary


def convert(start_goal_node, n):
    if start_goal_node == (0, infinity): return [0, n]
    elif start_goal_node == (infinity, 0): return [n, 0]
    else: return [0, 0]


def l1(v1, v2, n, owned_positions) -> int:
    """ computes L1 distance between v1 and v2 - L1 modified for the hexagonal grid """
    if v1 in start_goal_nodes and v2 in start_goal_nodes: return n

    if v1 in start_goal_nodes and v2 not in start_goal_nodes:
        v1 = convert(v1, n)

    if v2 in start_goal_nodes and v1 not in start_goal_nodes:
        v2 = convert(v2, n)

    rq_dictionary = r_q_dictionary(owned_positions)

    x0, y0 = v1[0], v1[1],
    x1, y1 = v2[0], v2[1]

    dx = x1 - x0
    dy = y1 - y0
    if np.sign(dx) == np.sign(dy):
        distance = abs(dx + dy)
    else:
        distance = max(abs(dx), abs(dy))

    for position in v1:
        distance -= rq_dictionary[position]

    for position in v2:
        distance -= rq_dictionary[position]
    return max(distance, 0)


def true_l1(v1, v2) -> int:
    """ computes L1 distance between v1 and v2 - L1 modified for the hexagonal grid """
    x0, y0 = v1[0], v1[1],
    x1, y1 = v2[0], v2[1]

    dx = x1 - x0
    dy = y1 - y0
    if np.sign(dx) == np.sign(dy):
        return abs(dx + dy)
    else:
        return max(abs(dx), abs(dy))


if __name__ == '__main__':
    # should be 0, as potential path can traverse along owned positions in a straight line
    owned_positions = [(1, 2), (2, 2), (3, 2), (4, 2), (5, 2)]
    estimate = l1((0, 2), (6, 2), 7, owned_positions)
    print(estimate == 0)

    estimate = l1((0, 2), (0, infinity), 7, owned_positions)
    print(estimate == 0)