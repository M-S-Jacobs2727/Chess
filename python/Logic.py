from .Piece import Piece, Rank, Color
from typing import Union


def initializeFromFEN(fenstring: str) -> list[Union[None, Piece]]:
    board = [None for _ in range(64)]
    char2rank = {
        "P": Rank.pawn,
        "N": Rank.knight,
        "B": Rank.bishop,
        "R": Rank.rook,
        "Q": Rank.queen,
        "K": Rank.king,
    }

    p = 0
    for c in fenstring.split()[0]:
        if c == "/":
            continue
        if c in "12345678":
            p += int(c)
            continue

        if c not in "PNBRQKpnbrqk":
            raise ValueError(f"Invalid character in FEN string: `{c}`")

        color = Color.white if c.isupper() else Color.black
        rank = char2rank[c.upper()]

        # FEN starts from black side of board,
        # but algebraic notation starts from white
        board[p] = Piece(rank, color)
        p += 1

    return board


def setup():
    classicFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = initializeFromFEN(classicFEN)
