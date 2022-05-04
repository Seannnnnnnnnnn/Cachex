""" file for testing child generation """
from agent.game_state import State

state = State("red", 5)
state.update("red", ("PLACE", 3, 0))
state.update("red", ("PLACE", 3, 1))
state.update("blue", ("PLACE", 4, 0))
state.print_state()
print("Generating Children ================")

for child in state.children():
    child.print_state()
