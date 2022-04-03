"""
COMP30024 Artificial Intelligence, Semester 1, 2022
Project Part A: Searching

This script contains the entry point to the program (the code in
`__main__.py` calls `main()`). Your solution starts here!
"""

import sys
import json
from typing import List, Tuple

from search.A_Star import A_Star
from search.heuristics import l1


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


def main():
    try:
        with open(sys.argv[1]) as file:
            data = json.load(file)
    except IndexError:
        print("usage: python3 -m search path/to/input.json", file=sys.stderr)
        sys.exit(1)

    start_pos = tuple(data['start'])
    goal_pos = tuple(data['goal'])
    block_pos = parse_blocks(data['board'])
    n = data['n']
    h = l1

    generate_solution(start_pos, goal_pos, h, n, block_pos)
