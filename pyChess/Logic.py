from pyChess import Piece, Rank, Color
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


def checkDirection(
    pieces: Pieces,
    niters: int,
    increment: int,
    king_index: int,
    attackingPieces: set[Piece],
    playerColor: Color,
):
    for i in range(1, niters + 1):
        piece = pieces[king_index + increment * i]
        if piece is None:
            continue
        if piece.color == playerColor:
            break
        if piece.rank in attackingPieces:
            return True
        break
    return False


def inCheck(pieces: Pieces, playerColor: Color):
    """Given the arrangement of `pieces`, returns `True` if the player with color
    `playerColor` is in check.
    """
    players_king = Piece(Rank.king, playerColor)
    king_index = pieces.index(players_king)
    king_col = king_index % 8
    king_row = king_index // 8

    lateral_pieces = {Rank.queen, Rank.rook}
    if king_col != 7:
        if checkDirection(
            pieces, 7 - king_col, 1, king_index, lateral_pieces, playerColor
        ):
            return True

    if king_col != 0:
        if checkDirection(
            pieces, king_col, -1, king_index, lateral_pieces, playerColor
        ):
            return True

    if king_row != 7:
        if checkDirection(
            pieces, 7 - king_row, 8, king_index, lateral_pieces, playerColor
        ):
            return True

    if king_row != 0:
        if checkDirection(
            pieces, king_row, -8, king_index, lateral_pieces, playerColor
        ):
            return True

    diagonal_pieces = {Rank.queen, Rank.bishop}
    if king_col != 7 and king_row != 7:
        if checkDirection(
            pieces,
            min(7 - king_row, 7 - king_col),
            9,
            king_index,
            diagonal_pieces
            if playerColor == Color.black
            else diagonal_pieces.union({Rank.pawn}),
            playerColor,
        ):
            return True

    if king_col != 0 and king_row != 7:
        if checkDirection(
            pieces,
            min(7 - king_row, king_col),
            7,
            king_index,
            diagonal_pieces
            if playerColor == Color.black
            else diagonal_pieces.union({Rank.pawn}),
            playerColor,
        ):
            return True

    if king_col != 7 and king_row != 0:
        if checkDirection(
            pieces,
            min(king_row, 7 - king_col),
            -7,
            king_index,
            diagonal_pieces
            if playerColor == Color.white
            else diagonal_pieces.union({Rank.pawn}),
            playerColor,
        ):
            return True

    if king_col != 0 and king_row != 0:
        if checkDirection(
            pieces,
            min(king_row, king_col),
            -9,
            king_index,
            diagonal_pieces
            if playerColor == Color.white
            else diagonal_pieces.union({Rank.pawn}),
            playerColor,
        ):
            return True

    # knights
    offsets = [-17, -15, -10, -6, 6, 10, 15, 17]
    col_ranges = [(1, 7), (0, 6), (2, 7), (0, 5), (2, 7), (0, 5), (1, 7), (0, 6)]
    row_ranges = [(2, 7), (2, 7), (1, 7), (1, 7), (0, 6), (0, 6), (0, 5), (0, 5)]
    for offset, col_range, row_range in zip(offsets, col_ranges, row_ranges):
        if (
            col_range[0] <= king_col <= col_range[1]
            and row_range[0] <= king_row <= row_range[1]
            and pieces[king_index + offset]
        ):
            if pieces[king_index + offset].rank == Rank.knight:
                return True

    return False


def getLegalMoves(pieces: Pieces, playerColor: Color, p=-1) -> set[str]:
    legalMoves = set()
    return legalMoves


def isaMove(
    pieces: Pieces, moveFrom: int, moveTo: int, lastMoveFrom: int, lastMoveTo: int
):
    piece = pieces[moveFrom]
    piece_row = moveFrom // 8
    piece_col = moveFrom % 8
    if piece.rank == Rank.knight:
        if abs(moveFrom - moveTo) not in [6, 10, 15, 17]:
            return False
    elif piece.rank == Rank.king:
        if abs(moveFrom - moveTo) not in [1, 7, 8, 9]:
            return False
        tmp_pieces = pieces.copy()
        tmp_pieces[moveTo] = Piece(Rank.king, piece.color)
        tmp_pieces[moveFrom] = None
        if inCheck(tmp_pieces, piece.color):
            return False
    elif piece.rank == Rank.rook:
        pass
    elif piece.rank == Rank.bishop:
        pass
    elif piece.rank == Rank.queen:
        pass
    else:  # pawn
        pass  # most complicated...

    return True


def makeMove(pieces: Pieces, oldIndex: int, newIndex: int):
    pass


def setup():
    classicFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    positions = [((i % 8) + 1, 8 - i // 8) for i in range(64)]
    pieces = initializeFromFEN(classicFEN)
