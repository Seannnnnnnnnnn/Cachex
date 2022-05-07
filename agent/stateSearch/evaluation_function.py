from search.A_Star import *
from search.heuristics import *
from agent.player import *
from agent.consts import *


def evaluation_func(player: str, state: State) -> int:
    playerscore = getscore(player, state)
    if player == "blue":
        computerscore = getscore("red", state)
        return playerscore - computerscore
    elif player == "red":
        computerscore = getscore("blue", state)
        return playerscore - computerscore


def getscore(turn: str, state: State) -> int:
    start = []
    end = []
    startscore = infinity
    endscore = infinity
    score = infinity
    if turn == "blue":
        for i in range(int(state.board_size)):
            start.append((state.board_size - 1, i))
            end.append((0, i))
        for point in state.get_positions("blue"):
            for endpoint in end:
                if endscore > len(A_Star(point, endpoint, l1, state.board_size, state.get_positions("red"))):
                    endscore = len(A_Star(point, endpoint, l1, state.board_size, state.get_positions("red")))
            for startpoint in start:
                if startscore > len(A_Star(point, startpoint, l1, state.board_size, state.get_positions("red"))):
                    startscore = len(A_Star(point, startpoint, l1, state.board_size, state.get_positions("red")))
            if score > (startscore + endscore):
                score = startscore + endscore
        return score
    elif turn == "red":
        for i in range(int(state.board_size)):
            start.append((i, state.board_size - 1))
            end.append((i, 0))
        for point in state.get_positions("red"):
            for endpoint in end:
                if endscore > len(A_Star(point, endpoint, l1, state.board_size, state.get_positions("blue"))):
                    endscore = len(A_Star(point, endpoint, l1, state.board_size, state.get_positions("blue")))
            for startpoint in start:
                if startscore > len(A_Star(point, startpoint, l1, state.board_size, state.get_positions("blue"))):
                    startscore = len(A_Star(point, startpoint, l1, state.board_size, state.get_positions("blue")))
            if score > (startscore + endscore):
                score = startscore + endscore
        return score
