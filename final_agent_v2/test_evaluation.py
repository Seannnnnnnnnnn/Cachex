from final_agent.game_state import State


state = State("red", 8)

state.update("red ", ("Place", 1, 7))
state.update("red ", ("Place", 2, 6))
state.update("red ", ("Place", 2, 5))
state.update("red ", ("Place", 3, 4))
state.update("red ", ("Place", 4, 3))
state.update("red ", ("Place", 5, 2))
state.update("red ", ("Place", 6, 2))
state.update("red ", ("Place", 7, 2))
state.update("red ", ("Place", 7, 0))


state.update("blue", ("Place", 0, 7))
state.update("blue", ("Place", 1, 5))
state.update("blue", ("Place", 1, 4))
state.update("blue", ("Place", 2, 3))
state.update("blue", ("Place", 3, 2))
state.update("blue", ("Place", 4, 1))
state.update("blue", ("Place", 4, 0))
state.update("blue", ("Place", 7, 7))


for child in state.children():
    print(child)
    print(child.evaluate("red"))

