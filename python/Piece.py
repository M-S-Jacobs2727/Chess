#from abc import ABC
from enum import Enum

class Rank(Enum):
    pawn = 1
    knight = 2
    bishop = 3
    rook = 4
    queen = 5
    king = 6

class Color(Enum):
    white = 1
    black = 2

class Piece:
    def __init__(self, col: int, row: int, rank: Rank, color: Color):
        self._pos = (col, row)
        self._rank = rank
        self._color = color
    
    @property
    def position(self):
        return self._pos
    
    @property
    def row(self):
        return self._pos[1]
    
    @property
    def col(self):
        return self._pos[0]

    @position.setter
    def position(self, col: int, row: int):
        self._pos = (col, row)

    @property
    def rank(self):
        return self._rank
    
    @rank.setter
    def rank(self, rank: Rank):
        if self._rank != Rank.pawn:
            raise TypeError("Cannot promote a piece that is not a pawn.")
        self._rank = rank
    
    @property
    def color(self):
        return self._color
