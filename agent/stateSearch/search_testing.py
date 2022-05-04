""" document for showing that search is working """
from agent.stateSearch.hueristics import l1
from agent.stateSearch.Modified_A_Star import A_Star


solution = A_Star("blue start", "blue goal", h=l1, n=6, blocks=[(0, 1), (1, 1), (1, 3), (3, 2)])
print(solution)
solution = A_Star("red start", "red goal", h=l1, n=6, blocks=[(0, 1), (1, 1), (1, 3), (3, 2)])
print(solution)
