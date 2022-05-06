""" file for testing the evaluation of a given state """
from agent.game_state import State


state = State("red", 5)
state.update("red", ("Place", 1, 2))
state.update("red", ("Place", 2, 2))
state.update("red", ("Place", 3, 2))
state.update("red", ("Place", 4, 2))

state.update("blue", ("Place", 3, 1))

state.print_state()

for child in state.children():
    child.print_state()
    print(child.evaluate("red"))


