"""
class containing the current state of the game

we represent the state of the game using a dictionary of tuples, with
board[(r,q)] = "" if it is unoccupied, or the color of the occupier
otherwise.

NOTE THE 0 INDEXING!
"""
from agent.util import print_board, opponent_color
from typing import List, Tuple
from random_group3.consts import neg_infinity, infinity, evaluation_function_v3
from random_group3.stateSearch.alpha_beta import alpha_beta_minimax
from random_group3.book_learning import move_book
from time import time


class State:
    def __init__(self, color, board_size, board=None):
        self.board_size = board_size
        self.color = color
        self.time_cap = self.board_size**2
        self.elapsed = 0
        self.ply = 0
        self.latest_action = None  # store the latest action we have received - this is used to derive optimal action
        self.center = (self.board_size//2, self.board_size//2)
        if board:
            self.board = board
        else:
            self.board = {}

    def __str__(self):
        return print_board(self.board_size, self.board)

    def update(self, color, action):
        """ updates the state of the game given action """
        self.latest_action = action
        self.ply += 1
        if action[0].upper() == "PLACE":
            r, q = action[1], action[2]
            self.board[(r, q)] = color
            self.check_capture(r, q, color)

        else:
            pos = next(iter(self.board))
            r, q = pos[0], pos[1]
            self.board[pos] = ""
            self.board[(q, r)] = "blue"

    def is_empty(self, r, q):
        return (r, q) not in self.board.keys() or self.board[(r, q)] == ""

    def is_terminal(self):
        evaluation = self.evaluate(self.color)
        return evaluation == neg_infinity or evaluation == infinity

    def children(self) -> List:
        """ generates all child positions of the current game state """
        children = []
        opponent = opponent_color(self.color)

        for r in range(self.board_size):
            for q in range(self.board_size):
                if self.is_empty(r, q):
                    child = State(opponent, self.board_size, self.board.copy())
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

    def get_positions(self, color: str) -> List[Tuple]:
        return [position for position in self.board.keys() if self.board[position] == color]

    def is_valid(self, point):
        r, q = point[0], point[1]
        return 0 <= r < self.board_size and 0 <= q < self.board_size

    def check_capture(self, r, q, color):
        """ checks if placing in position r q results in a capture """
        diamonds = [
            [(r - 1, q), (r + 1, q - 1), (r, q - 1)],  # first two are adjacent, last item in list is adjacent to (r,q)
            [(r+1, q), (r-1, q+1), (r, q+1)],
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

        points_to_delete = []
        for diamond in diamonds:
            points = self._validate_diamond(diamond, color)
            if points: points_to_delete += points

        for point in points_to_delete:
            self.board[point] = ""

    def _validate_diamond(self, diamond: List[Tuple], color):
        """
        validates if the capture rule is satisfied - if a key error is thrown then one of the spaces of the diamond
        is unoccupied, and therefore not satisfying the capture rule, so we just pass.
        """
        p1, p2 = diamond[0], diamond[1]
        p3 = diamond[2]
        try:
            if self.board[p1] == self.board[p2] and self.board[p3] == color and color != self.board[p1]\
                    and self.board[p3] != self.board[p1] and self.board[p2] != self.board[p3]:
                return [p1, p2]
        except KeyError: pass

    def get_branching_factor(self):
        # returns the number of occupied pieces as an approximate to branching factor.
        # Low occupied pieces => high branching factor
        occupied_pieces = len(self.get_positions(self.color)) + len(self.get_positions(opponent_color(self.color)))
        return occupied_pieces

    def generate_action_alpha_beta(self, depth):
        """ controls logic for deciding next action """

        t0 = time()

        # overwrite depth limit in the case of no time
        if self.board_size > 3 and self.time_cap - self.elapsed < 4.5: depth = 0

        if self.board_size > 3:
            action = move_book(self)
            if action: return action

        max_eval = neg_infinity
        action = None
        for child in self.children():
            # note we start with False as we are calling on a child node
            evaluation = alpha_beta_minimax(child, depth, neg_infinity, infinity, False, self.color)
            if evaluation >= max_eval:
                max_eval = evaluation
                action = child.latest_action
        t1 = time()
        self.elapsed += t1 - t0
        return action

    def evaluate(self, color):
        return evaluation_function_v3(self, color)
