"""
modified variant of the A* implementation found in the search module. includes a super source and super sink
node for both red and blue.
"""
from typing import List, Callable, Tuple
from collections import defaultdict
import heapq
from agent.consts import neg_infinity, infinity


start_goal_nodes = [(neg_infinity, 0), (infinity, 0), (0, neg_infinity), (0, infinity)]


def A_Star(start: str, goal: str, h: Callable, n: int, owned_positions: List[Tuple], blocks: List[Tuple] = []):
    """
    :param start: start node
    :param goal: goal node
    :param h: heuristic function
    :param n: board size (n x n)
    :param blocks: board size (n x n)
    :param owned_positions

    performs A* search on a given board, return 0 in the case there is no path between start and goal.
    The priority queue functionality required for the algorithm utilises a min-heap via the heapq library.
    We heappush tuples of (f_score(node), node) to maintain the heap based on f_score.
    nodes with lowest f_score are always at the top of the heap, so when pop() is called, the min is always produced
    """
    start, goal = get_start_goal_nodes(start, goal)
    discovered = []
    owned_positions_copy = owned_positions.copy()      # see line 64 for why we take a copy
    g_score, f_score, came_from = defaultdict(lambda: float('inf')), defaultdict(lambda: float('inf')), {}
    g_score[start], f_score[start] = 0, h(start, goal, n, owned_positions)

    heapq.heapify(discovered)
    heapq.heappush(discovered, (f_score[start], start))

    while len(discovered) > 0:
        current = heapq.heappop(discovered)[1]  # second element contains the (x,y) coordinates of the node
        if current == goal:
            return construct_solution(came_from, current, owned_positions_copy)

        for neighbor in get_neighbors(current, n, owned_positions):
            if legitimate(neighbor, n, blocks):  # if the neighbour node generated is a legitimate board position:

                tentative_score = g_score[current] + 1
                if tentative_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_score
                    f_score[neighbor] = tentative_score + h(neighbor, goal, n, owned_positions)

                    if neighbor not in discovered:
                        heapq.heappush(discovered, (f_score[neighbor], neighbor))
    return []


def construct_solution(came_from, current, owned_positions):
    """ produces solution path """
    total_path = [current]
    while current in came_from.keys():
        current = came_from[current]
        total_path.append(current)
    total_path.reverse()

    # for very specific test cases - some border positions that are owned appear in the path solution.
    # so, we just manually remove them
    for position in owned_positions:
        if position in total_path: total_path.remove(position)

    return total_path


def get_neighbors(node: Tuple[int], n: int, owned_positions: List[Tuple]) -> List[Tuple[int, int]]:
    """
    returns a list containing the neighbors of node - we check that the neighbor is valid when performing the search
    """
    if node in start_goal_nodes:
        neighbors = get_sink_node_neighbors(node, n)
    else:
        x, y = node[0], node[1]
        neighbors = [(x - 1, y), (x + 1, y), (x, y + 1), (x, y - 1), (x - 1, y + 1), (x + 1, y - 1)]

        for neighbor in neighbors:
            if neighbor in owned_positions:
                x, y = neighbor[0], neighbor[1]
                neighbors.remove(neighbor)
                owned_positions.remove(neighbor)
                neighbors += get_neighbors([x, y], n, owned_positions)

        if y == n - 1:  # blue edge of board
            neighbors.append((infinity, 0))

        if x == n - 1:  # red edge of board
            neighbors.append((0, infinity))
    return list(dict.fromkeys(neighbors))


def legitimate(node: Tuple[int, int], n: int, blocks: List[Tuple]) -> bool:
    """
    :param node: potential node
    :param n: board size
    :param blocks: contains (x,y) coordinates of occupied or 'blocked' spaces on the board

    the get_neighbors function generates all 6 adjacent positions any given node on a board. this function ensures that
    the position generated is legitimate, so we don't search position (-1, -1) for example
    """
    if node in blocks: return False
    if node in start_goal_nodes: return True
    for coordinate in node:
        if coordinate < 0 or coordinate >= n: return False
    return True


def get_sink_node_neighbors(node, n):
    if node == (neg_infinity, 0):
        return [(i, 0) for i in range(n)]
    elif node == (0, neg_infinity):
        return [(0, i) for i in range(n)]
    else:
        return []


def get_start_goal_nodes(start, end):
    """ we represent the start/end sink notes as tuples for consistency with heap-pop """
    if start == "blue start":
        return (neg_infinity, 0), (infinity, 0)
    elif start == "red start":
        return (0, neg_infinity), (0, infinity)
    else:
        return start, end


if __name__ == '__main__':
    positions = [(1, 2), (2, 2), (3, 2), (4, 2), (5, 2)]
    neighbors = get_neighbors((0, 2), 6, positions)
    print(neighbors)
