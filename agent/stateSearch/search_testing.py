""" document for showing that search is working """
from agent.stateSearch.hueristics import l1
from agent.stateSearch.Modified_A_Star import A_Star


solution = A_Star("blue start", "blue goal", h=l1, n=6, owned_positions=[], blocks=[(0, 0), (1, 0), (2, 0), (0, 3), (4, 2), (2, 3)])
print(solution)
solution = A_Star("red start", "red goal", h=l1, n=6, owned_positions=[], blocks=[(0, 1), (1, 1), (3, 0), (3, 2)])
print(solution)
solution = A_Star("red start", "red goal", h=l1, n=5, owned_positions=[(1, 0), (2, 0), (3, 0), (4, 0), (0, 0)], blocks=[])
print(solution)
