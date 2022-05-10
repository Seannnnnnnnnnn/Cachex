""" contains code for alpha-beta pruning """
from random_group3.consts import infinity, neg_infinity


def alpha_beta_minimax(position, depth, alpha, beta, maximising_player, color):
    if depth == 0 or position.is_terminal():
        evaluation = position.evaluate(color)
        state_dict[str(position)] = evaluation
        return evaluation

    if maximising_player:
        maxEval = neg_infinity
        for child in position.children():
            if str(child) in state_dict:
                eval = state_dict[str(child)]
            else:
                eval = alpha_beta_minimax(child, depth-1, alpha, beta, False, color)
            maxEval = max(maxEval, eval)
            if beta <= alpha:
                break
        return maxEval

    if not maximising_player:
        minEval = infinity
        for child in position.children():
            if str(child) in state_dict:
                eval = state_dict[str(child)]
            else:
                eval = alpha_beta_minimax(child, depth-1, alpha, beta, True, color)
            minEval = min(minEval, eval)
            if beta <= alpha:
                break
        return minEval


state_dict = {}
