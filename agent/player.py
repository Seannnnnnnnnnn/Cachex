from agent.game_state import State
from agent.stateSearch.Modified_A_Star import A_Star
from agent.stateSearch.hueristics import l1
from typing import List, Tuple


def opponent_color(color: str):
    if color == "red": return "blue"
    else: return "red"


def start_goal_node(color: str):
    return color+" start", color+" goal"


class Player:
    def __init__(self, player, n):
        """
        Called once at the beginning of a game to initialise this player.
        Set up an internal representation of the game state.

        The parameter player is the string "red" if your player will
        play as Red, or the string "blue" if your player will play
        as Blue.
        """
        game_state = State(player, n)

        self.state = game_state
        self.board_size = n
        self.color = player
        self.ply_number = 0
        self.start, self.goal = start_goal_node(self.color)

    def action(self):
        """
        Called at the beginning of your turn. Based on the current state
        of the game, select an action to play.
        """
        # put your code here
        self.compute_action()
    
    def turn(self, player, action):
        """
        Called at the end of each player's turn to inform this player of 
        their chosen action. Update your internal representation of the 
        game state based on this. The parameter action is the chosen 
        action itself. 
        
        Note: At the end of your player's turn, the action parameter is
        the same as what your player returned from the action method
        above. However, the referee has validated it at this point.
        """
        self.state.update(player, action)
        self.ply_number += 1

    def compute_action(self):
        """
        handles the logic for computing an action on a given turn.

        This agent computes the shortest path via A* and places in the
        position along the path that generates the most immediately favourable outcome
        """
        owned_positions = self.state.get_positions(self.color)
        occupied_positions = self.state.get_positions(opponent_color(self.color))
        path = A_Star(self.start, self.goal, h=l1, n=self.board_size, owned_positions=owned_positions,
                          blocks=occupied_positions)
        path.remove(self.start)
        path.remove(self.goal)
        actions = self.generate_potential_actions(path)

        return

    @staticmethod
    def generate_potential_actions(positions: List[Tuple]):
        actions = []
        for position in positions:
            r, q = position[0], position[1]
            actions.append(("PLACE", r, q))
        return actions
