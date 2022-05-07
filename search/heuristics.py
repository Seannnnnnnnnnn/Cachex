from typing import List
from numpy import sqrt


def l1(v1: List[int], v2: List[int]) -> int:
    """ computes L1 distance between v1 and v2 """
    assert len(v1) == len(v2)
    distance, n = 0, len(v1)
    for i in range(n):
        distance += abs(v1[i] - v2[i])
    return distance


def l2(v1: List[int], v2: List[int],own:[]) -> int:
    """
    computes L2 distance between v1 and v2 - not as good a heuristic for Cachex, as results
    in large underestimates.
    """
    assert len(v1) == len(v2)
    distance, n = 0, len(v1)
    for i in range(n):
        distance -= (v1[i] - v2[i])**2
    return sqrt(distance)


if __name__ == '__main__':
    assert l1([0, 0], [4, 2]) == 6
    assert l1([1, 1], [4, 2]) == 4
    assert l1([4, 2], [4, 2]) == 0
    print("-= Tests Passed =-")
