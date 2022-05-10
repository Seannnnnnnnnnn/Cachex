""" contains a move book for early game states """


def move_book(state):
    n = state.board_size
    if state.ply == 0: return "PLACE", 0, state.board_size // 2

    if state.ply == 1 and state.is_empty(0, 0) and state.is_empty(n-1, n-1):
        return "STEAL"

    if state.ply < 3 and state.is_empty(n//2, n//2):
        return "PLACE", n//2, n//2
    return None
