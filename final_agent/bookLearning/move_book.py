""" contains a class for moves """


def move_book(state):
    """ checks the move book to generate action for color """
    red_positions = state.get_positions("red")
    blu_positions = state.get_positions("blue")

    # take centre position early!
    if len(red_positions) + len(blu_positions) < 4 and state.ply > 1:
        r, q = state.board_size//2, state.board_size//2
        if state.is_empty(r, q): return "PLACE", r, q

    return  # State does not match anything in rule book - return None
