from search.A_Star import *
from search.heuristics import *
from referee.board import *
from agent.consts import *


def evaluation_func(player: str, board: Board) -> int:
    playerscore = getscore(player, board)
    if player == "blue":
        computerscore = getscore("red", board)
        return playerscore - computerscore
    elif player == "red":
        computerscore = getscore("blue", board)
        return playerscore - computerscore


def getscore(turn: str, board: Board) -> int:
    start = []
    end = []
    startscore = infinity
    endscore = infinity
    score = infinity
    if turn == "blue":
        for i in range(int(board.n)):
            start.append((board.n - 1, i))
            end.append((0, i))
        for point in board.blue:
            for endpoint in end:
                if endscore > len(A_Star(point, endpoint, l1, board.n, board.red)):
                    endscore = len(A_Star(point, endpoint, l1, board.n, board.red))
            for startpoint in start:
                if startscore > len(A_Star(point, startpoint, l1, board.n, board.red)):
                    startscore = len(A_Star(point, startpoint, l1, board.n, board.red))
            if score > (startscore + endscore):
                score = startscore + endscore
        return score
    elif turn == "red":
        for i in range(int(board.n)):
            start.append((i, board.n - 1))
            end.append((i, 0))
        for point in board.red:
            for endpoint in end:
                if endscore > len(A_Star(point, endpoint, l1, board.n, board.blue)):
                    endscore = len(A_Star(point, endpoint, l1, board.n, board.blue))
            for startpoint in start:
                if startscore > len(A_Star(point, startpoint, l1, board.n, board.blue)):
                    startscore = len(A_Star(point, startpoint, l1, board.n, board.blue))
            if score > (startscore + endscore):
                score = startscore + endscore
        return score
