from enum import Enum
from copy import deepcopy


class Piece:
    def __init__(self, piece_type):
        self.piece_type = piece_type
        if piece_type is PieceType.I:
            self.matrix = [
                [0, 0, 0, 0],
                [1, 1, 1, 1],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ]
        elif piece_type is PieceType.J:
            self.matrix = [
                [2, 0, 0],
                [2, 2, 2],
                [0, 0, 0]
            ]
        elif piece_type is PieceType.L:
            self.matrix = [
                [0, 0, 3],
                [3, 3, 3],
                [0, 0, 0]
            ]
        elif piece_type is PieceType.O:
            self.matrix = [
                [4, 4],
                [4, 4]
            ]
        elif piece_type is PieceType.S:
            self.matrix = [
                [0, 5, 5],
                [5, 5, 0],
                [0, 0, 0]
            ]
        elif piece_type is PieceType.T:
            self.matrix = [
                [0, 6, 0],
                [6, 6, 6],
                [0, 0, 0]
            ]
        else:
            self.matrix = [
                [7, 7, 0],
                [0, 7, 7],
                [0, 0, 0]
            ]

        self.x = int((10 - len(self.matrix[0]))/2)
        self.y = 20 - len(self.matrix)


class PieceType(Enum):
    # Pieces
    I = 1
    J = 2
    L = 3
    O = 4
    S = 5
    T = 6
    Z = 7

    @classmethod
    def get_color(cls, piece_type):
        if piece_type is PieceType.I:
            return 0, 200, 255
        elif piece_type is PieceType.J:
            return 0, 0, 255
        elif piece_type is PieceType.L:
            return 255, 100, 0
        elif piece_type is PieceType.O:
            return 255, 255, 0
        elif piece_type is PieceType.S:
            return 0, 255, 0
        elif piece_type is PieceType.T:
            return 255, 0, 255
        else:
            return 255, 0, 0
