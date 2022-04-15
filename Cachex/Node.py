"""
Contains Node class for building out state of each board position
"""


class Node:
    def __init__(self, x: int, y: int, color=None):
        self.x = x
        self.y = y
        self.color = color

    def __str__(self):
        return f"({self.x},{self.y})"

    def set_color(self, color: str):
        assert color == "red" or color == "blue"
        self.color = color
