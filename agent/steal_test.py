""" tests the steal rule is functioning """
from agent.game_state import State

state = State("blue", 5)
state.update("red", ("Place", 3, 2))
print(state)

state.update("blue", ("Steal", ))
print("testing steal")
print(state)

print("=================================")

state = State("blue", 5)
state.update("red", ("Place", 0, 0))
print(state)

state.update("blue", ("Steal", ))
print("testing steal")
print(state)

print("=================================")

state = State("blue", 5)
state.update("red", ("Place", 4, 4))
print(state)

state.update("blue", ("Steal", ))
print("testing steal")
print(state)


print("=================================")

state = State("blue", 5)
state.update("red", ("Place", 0, 4))
print(state)

state.update("blue", ("Steal", ))
print("testing steal")
print(state)

print("=================================")

state = State("blue", 5)
state.update("red", ("Place", 2, 2))
print(state)

state.update("blue", ("Steal", ))
print("testing steal")
print(state)