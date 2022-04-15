""" contains code for alpha-beta pruning """
from agent.consts import *


def alpha_beta_minimax(position, depth, alpha, beta, maximising_player):
    if depth == 0 or position.isTerminal():
        return evaluation_func(position)

    if maximising_player:
        maxEval = neg_infinity
        for child in position.children():
            eval = alpha_beta_minimax(child, depth-1, alpha, beta, False)
            maxEval = max(maxEval, eval)
            if beta <= alpha:
                break
        return maxEval

    if not maximising_player:
        minEval = infinity
        for child in position.children():
            eval = alpha_beta_minimax(child, depth-1, alpha, beta, True)
            minEval = min(minEval, eval)
            if beta <= alpha:
                break
        return minEval
