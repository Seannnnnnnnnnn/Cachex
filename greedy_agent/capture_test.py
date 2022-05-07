from greedy_agent.game_state import State

state = State("red", 9)
state.update("r", ("place", 0, 8))
state.update("r", ("place", 0, 7))
state.update("r", ("place", 1, 6))
state.update("r", ("place", 1, 8))
state.update("r", ("place", 2, 6))
state.update("b", ("place", 3, 6))
state.update("b", ("place", 3, 7))
state.update("b", ("place", 1, 7))
state.update("r", ("place", 4, 6))

print(state)

state.update("r", ("place", 2, 7))
print(state)