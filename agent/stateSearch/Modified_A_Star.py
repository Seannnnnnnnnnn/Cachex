from typing import List, Callable, Tuple
from collections import defaultdict
import heapq


def A_Star(start: str, goal: str, h: Callable, n: int, blocks: List[Tuple] = []):
    """
    :param start: start node
    :param goal: goal node
    :param h: heuristic function
    :param n: board size (n x n)
    :param blocks: board size (n x n)

    performs A* search on a given board, return 0 in the case there is no path between start and goal.
    The priority queue functionality required for the algorithm utilises a min-heap via the heapq library.
    We heappush tuples of (f_score(node), node) to maintain the heap based on f_score.
    nodes with lowest f_score are always at the top of the heap, so when pop() is called, the min is always produced
    """
    discovered = []
    g_score, f_score, came_from = defaultdict(lambda: float('inf')), defaultdict(lambda: float('inf')), {}
    g_score[start], f_score[start] = 0, h(start, goal, n)

    heapq.heapify(discovered)
    heapq.heappush(discovered, (f_score[start], start))

    while len(discovered) > 0:

        current = heapq.heappop(discovered)[1]  # second element contains the (x,y) coordinates of the node

        if current == goal:
            return construct_solution(came_from, current)

        for neighbor in get_neighbors(current, n):
            if legitimate(neighbor, n, blocks):  # if the neighbour node generated is a legitimate board position:

                tentative_score = g_score[current] + 1
                if tentative_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_score
                    f_score[neighbor] = tentative_score + h(neighbor, goal, n)

                    if neighbor not in discovered:
                        heapq.heappush(discovered, (f_score[neighbor], neighbor))
    return []


def construct_solution(came_from, current):
    """ produces solution path """
    total_path = [current]
    while current in came_from.keys():
        current = came_from[current]
        total_path.append(current)
    total_path.reverse()
    return total_path


def get_neighbors(node: List[int], n: int) -> List[Tuple[int, int]]:
    """
    returns a list containing the neighbors of node - we check that the neighbor is valid when performing the search
    """
    if type(node) == str:
        neighbors = get_sink_node_neighbors(node, n)
    else:
        x, y = node[0], node[1]
        neighbors = [(x - 1, y), (x + 1, y), (x, y + 1), (x, y - 1), (x - 1, y + 1), (x + 1, y - 1)]

        if y == n - 1:  # blue edge of board
            neighbors.append("blue goal")

        if x == n - 1:  # red edge of board
            neighbors.append("red goal")
    return neighbors


def legitimate(node: Tuple[int, int], n: int, blocks: List[Tuple]) -> bool:
    """
    :param node: potential node
    :param n: board size
    :param blocks: contains (x,y) coordinates of occupied or 'blocked' spaces on the board

    the get_neighbors function generates all 6 adjacent positions any given node on a board. this function ensures that
    the position generated is legitimate, so we don't search position (-1, -1) for example
    """
    if node in blocks: return False
    if type(node) == str: return True
    for coordinate in node:
        if coordinate < 0 or coordinate >= n: return False
    return True


def get_sink_node_neighbors(node, n):
    if node == "blue start":
        return [(i, 0) for i in range(n)]
    elif node == "red start":
        return [(0, i) for i in range(n)]
    else:
        return []


if __name__ == '__main__':
    from agent.stateSearch.hueristics import l1
    solution = A_Star("blue start", "blue goal", h=l1, n=5, blocks=[(0, 1), (1, 1), (1, 3), (3, 2)])
    print(solution)
    solution = A_Star("red start", "red goal", h=l1, n=5, blocks=[(0, 1), (1, 1), (1, 3), (3, 2)])
    print(solution)

