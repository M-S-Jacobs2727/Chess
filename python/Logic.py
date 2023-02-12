from .Piece import Piece, Rank, Color
from typing import Union


Pieces = list[Union[None, Piece]]


def initializeFromFEN(fenstring: str) -> Pieces:
    pieces = [None for _ in range(64)]
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
        pieces[p] = Piece(rank, color)
        p += 1

    return pieces


def checkDirection(pieces: Pieces, niters: int, increment: int, king_index: int, attackingPieces: set[Piece], playerColor: Color):
    for i in range(1, niters+1):
        piece = pieces[king_index + increment*i]
        if piece is None:
            continue
        if piece.color == playerColor:
            break
        if piece.rank in attackingPieces:
            return True
        break
    return False


def inCheck(pieces: Pieces, playerColor: Color, move: str = ""):
    players_king = Piece(Rank.king, playerColor)
    king_index = pieces.index(players_king)
    king_col = king_index % 8
    king_row = king_index // 8

    if king_col != 7:
        if checkDirection(pieces, 7-king_col, 1, king_index, {Rank.queen, Rank.rook}, playerColor):
            return True
    
    if king_col != 0:
        if checkDirection(pieces, king_col, -1, king_index, {Rank.queen, Rank.rook}, playerColor):
            return True
    
    if king_row != 7:
        if checkDirection(pieces, 7-king_row, 8, king_index, {Rank.queen, Rank.rook}, playerColor):
            return True
    
    if king_row != 0:
        if checkDirection(pieces, king_row, -8, king_index, {Rank.queen, Rank.rook}, playerColor):
            return True
    
    if king_col != 7 and king_row != 7:
        if checkDirection(pieces, king_row, 9, king_index, {Rank.queen, Rank.bishop}, playerColor):
            return True


def getLegalMoves(pieces: Pieces, player: Color, p=-1) -> set[str]:
    legalMoves = set()
    return legalMoves


def setup():
    classicFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    positions = [((i%8)+1, 8-i//8) for i in range(64)]
    pieces = initializeFromFEN(classicFEN)
