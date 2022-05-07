""" contains constants """
import math

infinity = float('inf')
neg_infinity = float('-inf')


def sigmoid(x):
    return 1 / (1 + math.exp(-x))

