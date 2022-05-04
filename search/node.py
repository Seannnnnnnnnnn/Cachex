""" contains a class for a node on the board """


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = None

    def capture(self, color):
        self.color = color
