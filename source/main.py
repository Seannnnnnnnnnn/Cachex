"""
Main file for submission in Part A of the project. Reads in json input file from standard input, parses json
to construct a board, and then calls A* search to perform an optimal path search. When A* terminates with optimal
path, path length and sequence of positions on the board are written to output file solution.txt
"""
import json
from typing import List, Tuple
from Cachex.A_Star import A_Star
from Cachex.heuristics import l1


def parse_blocks(board: List[List]) -> List[Tuple]:
    """ parses road blocks from json input """
    blocks = []
    for position in board:
        x, y = position[1], position[2]
        blocks.append((x, y))
    return blocks


def generate_solution(start, goal, heuristic, board_size, road_blocks):
    """ generates solution using A* search, then prints to standard output """
    solution = A_Star(start, goal, heuristic, board_size, road_blocks)
    with open("solution.txt", mode="w") as outfile:
        outfile.write(str(len(solution))+"\n")
        for coordinate in solution:
            outfile.write(str(coordinate)+"\n")
    return


if __name__ == '__main__':
    # TODO update below to accept from command line
    path = "source/sample_input.json"
    with open(path) as file:
        data = json.load(file)

    start_pos = tuple(data['start'])
    goal_pos = tuple(data['goal'])
    block_pos = parse_blocks(data['board'])
    n = data['n']
    h = l1

    generate_solution(start_pos, goal_pos, h, n, block_pos)
