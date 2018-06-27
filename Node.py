# Класс вершины дерева Хаффмана
class Node:
    symbol = None
    left = None
    right = None

    def __init__(self, symbol=None, left=None, right=None):
        self.symbol = symbol
        self.left = left
        self.right = right

    def __lt__(self, other):
        return False