"""
class containing the current state of the game

we represent the state of the game using a dictionary of tuples, with
board[(r,q)] = "" if it is unoccupied, or the color of the occupier
otherwise.

NOTE THE 0 INDEXING!
"""
from agent.util import *
from typing import List, Tuple


class State:
    def __init__(self, color, board_size, board=None):
        self.board_size = board_size
        self.color = color
        if board:
            self.board = board
        else:
            self.board = {}

    def update(self, color, action):
        """ updates the state of the game given action """
        if action[0].upper() == "PLACE":
            r, q = action[1], action[2]
            self.board[(r, q)] = color
            self.check_capture(r, q, color)

        if action[0].upper() == "STEAL":
            mid = int(self.board_size/2)
            self.board[(mid, mid)] = "Blue"

    def is_empty(self, r, q):
        return (r, q) not in self.board.keys() or self.board[(r, q)] == ""

    def print_state(self):
        print_board(self.board_size, self.board)

    def children(self) -> List:
        """ generates all child positions of the current game state """
        children = []

        for r in range(self.board_size):
            for q in range(self.board_size):
                if self.is_empty(r, q):
                    child = State(self.color, self.board_size, self.board.copy())
                    child.update(self.color, ("PLACE", r, q))
                    children.append(child)
        return children

    def board_list(self):
        """ converts the state of the board into a list of lists """
        board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        for position in self.board.keys():
            r, q = position[0], position[1]
            board[r][q] = self.board[position]
        return board

    def is_valid(self, point):
        r, q = point[0], point[1]
        return 0 <= r < self.board_size and 0 <= q < self.board_size

    def check_capture(self, r, q, color):
        """ checks if placing in position r q results in a capture """
        diamonds = [
            [(r - 1, q), (r + 1, q - 1), (r, q - 1)],  # first two are adjacent, last item in list is adjacent to (r,q)
            [(r, q - 1), (r + 1, q), (r + 1, q - 1)],
            [(r + 1, q - 1), (r, q + 1), (r + 1, q)],
            [(r - 1, q), (r, q + 1), (r - 1, q + 1)],
            [(r, q - 1), (r - 1, q + 1), (r - 1, q)],
            [(r, q - 1), (r + 1, q - 1), (r + 1, q - 2)],
            [(r + 1, q - 1), (r + 1, q), (r + 2, q - 1)],
            [(r + 1, q), (r, q + 1), (r + 1, q + 1)],
            [(r, q + 1), (r - 1, q + 1), (r - 1, q + 2)],
            [(r - 1, q), (r - 1, q + 1), (r - 2, q + 1)],
            [(r, q - 1), (r - 1, q), (r - 1, q - 1)]
        ]

        for diamond in diamonds:
            self._validate_diamond(diamond, color)

    def _validate_diamond(self, diamond: List[Tuple], color):
        """
        validates if the capture rule is satisfied - if a key error is thrown then one of the spaces of the diamond
        is unoccupied, and therefore not satisfying the capture rule, so we just pass.
        """
        p1, p2 = diamond[0], diamond[1]
        p3 = diamond[2]
        try:
            if self.board[p1] == self.board[p2] and self.board[p3] == color:
                self.board[p1] = ""
                self.board[p2] = ""
        except KeyError: pass
