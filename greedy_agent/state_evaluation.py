from greedy_agent.game_state import State
from agent.consts import evaluation_function_v2

print("testing standard evaluation")
state = State("red", 6)
state.update("red", ("place", 2, 2))
state.update("blue", ("place", 3, 0))
state.update("blue", ("place", 3, 2))

print(state)

state.update("red", ("place", 0, 0))

print(state)
print(evaluation_function_v2(state, "red"))