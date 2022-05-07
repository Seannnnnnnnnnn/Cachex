"""
class containing the current state of the game

we represent the state of the game using a dictionary of tuples, with
board[(r,q)] = "" if it is unoccupied, or the color of the occupier
otherwise.

NOTE THE 0 INDEXING!
"""
from agent.util import print_board, opponent_color, start_goal_node
from typing import List, Tuple
from agent.stateSearch.Modified_A_Star import A_Star
from agent.stateSearch.hueristics import l1
from agent.stateSearch.alpha_beta import alpha_beta_minimax
from agent.consts import sigmoid, neg_infinity, infinity


class State:
    def __init__(self, color, board_size, board=None):
        self.board_size = board_size
        self.color = color
        self.ply_number = 0
        self.latest_action = None  # store the latest action we have received - this is used to derive optimal action
        if board:
            self.board = board
        else:
            self.board = {}

    def __str__(self):
        return print_board(self.board_size, self.board)

    def update(self, color, action):
        """ updates the state of the game given action """
        self.latest_action = action
        self.ply_number += 1
        if action[0].upper() == "PLACE":
            r, q = action[1], action[2]
            self.board[(r, q)] = color
            self.check_capture(r, q, color)

        if action[0].upper() == "STEAL":
            pos = next(iter(self.board))
            r, q = pos[0], pos[1]
            self.board[pos] = ""
            self.board[(self.board_size-r-1, self.board_size-q-1)] = "blue"

    def is_empty(self, r, q):
        return (r, q) not in self.board.keys() or self.board[(r, q)] == ""

    def is_terminal(self):
        return self.evaluate(self.color) == 1 or self.evaluate(self.color) == -1

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

    def generate_action_alpha_beta(self):
        """ controls the logic for deciding the next action """
        max_eval = neg_infinity
        action = None
        for child in self.children():
            evaluation = alpha_beta_minimax(child, 2, neg_infinity, infinity, True)
            if evaluation > max_eval:
                max_eval = evaluation
                action = child.latest_action
        return action

    def evaluate_action(self, color, action):
        """
        produces a dummy state following each action and returns an evaluation of it
        """
        child = State(self.color, self.board_size, self.board.copy())
        child.update(color, action)
        return child.evaluate(color)

    def evaluate(self, color):
        """
        evaluation of the state from the perspective of given color
        """
        opponent = opponent_color(color)

        owned_positions = self.get_positions(color)
        opponent_positions = self.get_positions(opponent)

        agent_path_length = self.num_plays_to_win(color)
        opponent_path_length = self.num_plays_to_win(opponent)

        if opponent_path_length == 0:  # this occurs when agent forms a wall from one side to the other
            return 1
        elif agent_path_length == 0:
            return -1
        else:
            net_path_length = agent_path_length - opponent_path_length
            net_piece_count = len(owned_positions) - len(opponent_positions)
            return sigmoid(net_path_length + 0.5*net_piece_count)

    def num_plays_to_win(self, color):
        """
        computes the number of plays required for color to win. We subtract 2 as path includes start and goal node
        """
        opponent = opponent_color(color)

        owned_positions = self.get_positions(color)
        opponent_positions = self.get_positions(opponent)

        start, goal = start_goal_node(color)
        path = A_Star(start, goal, h=l1, n=self.board_size, owned_positions=owned_positions,
                      blocks=opponent_positions)
        return len(path)
