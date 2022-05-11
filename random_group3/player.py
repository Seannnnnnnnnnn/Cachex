from random_group3.game_state import State


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

    def action(self):
        """
        Called at the beginning of your turn. Based on the current state
        of the game, select an action to play.
        """
        depth = self._compute_depth(self.state.ply)
        action = self.state.generate_action_alpha_beta(depth)
        return action
    
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

    @staticmethod
    def _compute_depth(ply):
        if ply < 10:
            return 2
        else: return 1

