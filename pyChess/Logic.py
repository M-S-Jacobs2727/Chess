from pyChess import Piece, Rank, Color
import re
from typing import Union


Board = list[Union[None, Piece]]


def checkValidBoard(board: Board) -> None:
    pass


def checkValidFENString(fenstring: str) -> None:
    splitstring = fenstring.split()
    if len(splitstring) != 1 and len(splitstring) != 6:
        raise SyntaxError(f"Invalid number of fields in FEN string: {len(splitstring)}. Should be 1 or 6.")
    boardonly = len(splitstring) == 1
    if boardonly:
        boardstring = splitstring[0]
        turncolor = castle = enpassant = halfturn = fullturn = None
    else:
        boardstring, turncolor, castle, enpassant, halfturn, fullturn = splitstring

    rows = boardstring.split("/")
    if len(rows) != 8:
        raise SyntaxError(f"Invalid number of rows in FEN string: {len(rows)}. Should be 8.")
    numblackkings = 0
    numwhitekings = 0
    for row in rows:
        counter = 0
        for c in row:
            if c.upper() in "PNBQR":
                counter += 1
            elif c in "12345678":
                counter += int(c)
            elif c == "k":
                counter += 1
                numblackkings += 1
            elif c == "K":
                counter += 1
                numwhitekings += 1
            else:
                raise SyntaxError(f"Invalid character in FEN string: `{c}`")
        
        if counter != 8:
            raise SyntaxError(f"Invalid number of columns in row: {row}. Should be 8, found {counter}.")
    if numblackkings != 1 or numwhitekings != 1:
        raise ValueError(f"Wrong number of kings found in FEN string. Should be 1 black and 1 white, found {numblackkings} black and {numwhitekings} white.")
    
    if not boardonly:
        if turncolor not in "wb" or len(turncolor) != 1:
            raise SyntaxError(f"Invalid turn color character, should be 'w' or 'b', found '{turncolor}'.")
        if not re.fullmatch(r"(K?Q?k?q?|-)", castle):
            raise SyntaxError(f"Invalid castle availablity in FEN string. Should be subset of 'KQkq' or '-', found '{castle}'.")
        if not re.fullmatch(r"([a-h][36]|-)", enpassant):
            raise SyntaxError(f"Invalid en passant target in FEN string. Should be a square on the 3rd or 6th rank, or '-', found '{enpassant}'.")
        if not re.fullmatch(r"[0-9]+", halfturn):
            raise SyntaxError(f"Invalid half-turn clock. Should be an integer, found '{halfturn}'.")
        if not re.fullmatch(r"[1-9][0-9]*", fullturn):
            raise SyntaxError(f"Invalid full-turn clock. Should be an integer, found '{fullturn}'.")
    

def initializeFromFEN(fenstring: str) -> Board:
    checkValidFENString(fenstring)
    board: Board = [None for _ in range(64)]
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
    
    checkValidBoard(board)

    return board


def checkDirection(
    board: Board,
    niters: int,
    increment: int,
    king_index: int,
    attackingPieces: set[Piece],
    playerColor: Color,
):
    i = 1
    piece = board[king_index + increment]
    while piece is None and i < niters:
        i += 1
        piece = board[king_index + increment*i]
    if piece is None:
        return False
    return piece.rank in attackingPieces and piece.color != playerColor


def inCheck(board: Board, playerColor: Color):
    """Given the arrangement of `pieces`, returns `True` if the player with color
    `playerColor` is in check.
    """
    players_king = Piece(Rank.king, playerColor)
    king_index = board.index(players_king)
    king_col = king_index % 8
    king_row = king_index // 8

    lateral_pieces = {Rank.queen, Rank.rook}
    if king_col != 7:
        if checkDirection(
            board, 7 - king_col, 1, king_index, lateral_pieces, playerColor
        ):
            return True

    if king_col != 0:
        if checkDirection(
            board, king_col, -1, king_index, lateral_pieces, playerColor
        ):
            return True

    if king_row != 7:
        if checkDirection(
            board, 7 - king_row, 8, king_index, lateral_pieces, playerColor
        ):
            return True

    if king_row != 0:
        if checkDirection(
            board, king_row, -8, king_index, lateral_pieces, playerColor
        ):
            return True

    diagonal_pieces = {Rank.queen, Rank.bishop}
    if king_col != 7 and king_row != 7:
        if checkDirection(
            board,
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
            board,
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
            board,
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
            board,
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
            and board[king_index + offset]
        ):
            if board[king_index + offset].rank == Rank.knight:
                return True

    return False


def getLegalMoves(pieces: Board, playerColor: Color, p=-1) -> set[str]:
    legalMoves = set()
    return legalMoves


def isaMove(
    pieces: Board, moveFrom: int, moveTo: int, lastMoveFrom: int, lastMoveTo: int
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


def makeMove(pieces: Board, oldIndex: int, newIndex: int):
    pass


def setup():
    classicFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    positions = [((i % 8) + 1, 8 - i // 8) for i in range(64)]
    pieces = initializeFromFEN(classicFEN)
