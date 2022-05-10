""" contains constants """
infinity = float('inf')
neg_infinity = float('-inf')

import math
from agent.util import opponent_color, start_goal_node
from agent.stateSearch.Modified_A_Star import A_Star
from agent.stateSearch.hueristics import l1


def evaluation_function_v1(state, color: str):
    """
    evaluation function for a given game state and color
    features are:

    path length to win: returns the inverse of the path length to win, so places that minimise the
    required additional path length are considered good.
    """

    opponent = opponent_color(color)
    n = state.board_size

    owned_positions = state.get_positions(color)
    opponent_positions = state.get_positions(opponent)

    start, goal = start_goal_node(color)
    num_plays_to_win = A_Star(start, goal, h=l1, n=state.board_size, owned_positions=owned_positions,
                              blocks=opponent_positions)

    return n - len(num_plays_to_win)


def evaluation_function_v2(state, color: str, debug=False):
    """
    evaluation function for a given game state and color
    features:
    path length to win: returns the inverse of the path length to win, so places that minimise the
    required additional path length are considered good.

    path length to lose: consider the number of moves that the opponent has to make to win. Then return as the
    difference of these two
    """
    opponent = opponent_color(color)

    owned_positions = state.get_positions(color)
    opponent_positions = state.get_positions(opponent)

    start, goal = start_goal_node(color)
    opponent_start, opponent_goal = start_goal_node(opponent)

    num_plays_to_win = A_Star(start, goal, h=l1, n=state.board_size,
                              owned_positions=owned_positions.copy(), blocks=opponent_positions)

    if not num_plays_to_win: return neg_infinity

    num_plays_to_lose = A_Star(opponent_start, opponent_goal, h=l1, n=state.board_size,
                               owned_positions=opponent_positions, blocks=owned_positions)

    if not num_plays_to_lose: return infinity

    if debug:
        print(f"num plays to win:  {len(num_plays_to_win)-2}\nnum plays to lose: {len(num_plays_to_lose)-2}")
        print(f"path to win:  {num_plays_to_win}\npath to lose: {num_plays_to_lose}")

    return (len(num_plays_to_lose)-2) - (len(num_plays_to_win)-2)


def evaluation_function_v3(state, color: str, debug=False):
    """
    evaluation function for a given game state and color
    features:
    path length to win: returns the inverse of the path length to win, so places that minimise the
    required additional path length are considered good.

    path length to lose: consider the number of moves that the opponent has to make to win. Then return as the
    difference of these two
    """
    opponent = opponent_color(color)

    owned_positions = state.get_positions(color)
    opponent_positions = state.get_positions(opponent)

    start, goal = start_goal_node(color)
    opponent_start, opponent_goal = start_goal_node(opponent)

    num_plays_to_win = A_Star(start, goal, h=l1, n=state.board_size,
                              owned_positions=owned_positions.copy(), blocks=opponent_positions)

    if not num_plays_to_win: return neg_infinity

    num_plays_to_lose = A_Star(opponent_start, opponent_goal, h=l1, n=state.board_size,
                               owned_positions=opponent_positions, blocks=owned_positions)

    if not num_plays_to_lose: return infinity

    if debug:
        print(f"num plays to win:  {len(num_plays_to_win)-2}\nnum plays to lose: {len(num_plays_to_lose)-2}")
        print(f"path to win:  {num_plays_to_win}\npath to lose: {num_plays_to_lose}")

    net_position = (len(num_plays_to_lose)-2) - (len(num_plays_to_win)-2)
    net_pieces = len(owned_positions) - len(owned_positions)

    return net_position + 0.25*net_pieces

