# from abc import ABC
from collections import namedtuple
from enum import Enum, IntEnum, auto


Piece = namedtuple("Piece", ["rank", "color"])


class Rank(Enum):
    pawn = auto()
    knight = auto()
    bishop = auto()
    rook = auto()
    queen = auto()
    king = auto()


class Color(IntEnum):
    white = -1
    black = 1


# class Piece:
#     def __init__(self, col: int, row: int, rank: Rank, color: Color):
#         self._pos = (col, row)
#         self._rank = rank
#         self._color = color

#     @property
#     def position(self):
#         return self._pos

#     @property
#     def row(self):
#         return self._pos[1]

#     @property
#     def col(self):
#         return self._pos[0]

#     @position.setter
#     def position(self, col: int, row: int):
#         self._pos = (col, row)

#     @property
#     def rank(self):
#         return self._rank

#     @rank.setter
#     def rank(self, rank: Rank):
#         if self._rank != Rank.pawn:
#             raise TypeError("Cannot promote a piece that is not a pawn.")
#         self._rank = rank

#     @property
#     def color(self):
#         return self._color
