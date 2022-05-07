""" tests that the agent is calling things correctly """
from agent.player import Player

player = Player("blue", 6)
action = player.action()


print(action)
