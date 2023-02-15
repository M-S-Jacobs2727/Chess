from pyChess import Piece, Rank, Color
from collections import namedtuple
from dataclasses import dataclass, field
import re
from typing import Union, Optional


Board = list[Union[None, Piece]]


def emptyBoard() -> Board:
    return [None for _ in range(64)]


@dataclass(order=True)
class GameState:
    fullturn: int = field(default=1)
    turn: Color = field(default=Color.white)
    board: Board = field(compare=False, default_factory=emptyBoard)
    castleavail: int = field(compare=False, default=15)
    enpassant: int = field(compare=False, default=-1)
    halfturn: int = field(compare=False, default=0)


def checkValidBoard(board: Board) -> None:
    """Checks if both kings are in check, if there are pawns on the 1st or 8th ranks,
    or if the kings are touching.
    """
    pass


def checkValidFENString(fenstring: str) -> None:
    splitstring = fenstring.split()
    if len(splitstring) != 1 and len(splitstring) != 6:
        raise SyntaxError(
            f"Invalid number of fields in FEN string: {len(splitstring)}. Should be 1 or 6."
        )
    boardonly = len(splitstring) == 1
    if boardonly:
        boardstring = splitstring[0]
        turncolor = castle = enpassant = halfturn = fullturn = None
    else:
        boardstring, turncolor, castle, enpassant, halfturn, fullturn = splitstring

    rows = boardstring.split("/")
    if len(rows) != 8:
        raise SyntaxError(
            f"Invalid number of rows in FEN string: {len(rows)}. Should be 8."
        )
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
            raise SyntaxError(
                f"Invalid number of columns in row: {row}."
                f" Should be 8, found {counter}."
            )
    if numblackkings != 1 or numwhitekings != 1:
        raise ValueError(
            "Wrong number of kings found in FEN string. Should be 1 black and 1 white,"
            f" found {numblackkings} black and {numwhitekings} white."
        )

    if not boardonly:
        if turncolor not in "wb" or len(turncolor) != 1:
            raise SyntaxError(
                "Invalid turn color character, should be 'w' or 'b',"
                f" found '{turncolor}'."
            )
        if not re.fullmatch(r"(K?Q?k?q?|-)", castle):
            raise SyntaxError(
                "Invalid castle availablity in FEN string. Should be subset of"
                f" 'KQkq' or '-', found '{castle}'."
            )
        if not re.fullmatch(r"([a-h][36]|-)", enpassant):
            raise SyntaxError(
                "Invalid en passant target in FEN string. Should be a square on the"
                f" 3rd or 6th rank, or '-', found '{enpassant}'."
            )
        if not re.fullmatch(r"[0-9]+", halfturn):
            raise SyntaxError(
                f"Invalid half-turn clock. Should be an integer, found '{halfturn}'."
            )
        if not re.fullmatch(r"[1-9][0-9]*", fullturn):
            raise SyntaxError(
                f"Invalid full-turn clock. Should be an integer, found '{fullturn}'."
            )


def initializeFromFEN(fenstring: str) -> GameState:
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

    splitstring = fenstring.split()
    p = 0
    for c in splitstring[0]:
        if c in "12345678":
            p += int(c)
        elif c != "/":
            color = Color.white if c.isupper() else Color.black
            rank = char2rank[c.upper()]

            board[p] = Piece(rank, color)
            p += 1

    checkValidBoard(board)
    if len(splitstring) > 1:
        turn = Color.white if splitstring[1] == "w" else Color.black
        castleavail = 0
        for i, c in "KQkq":
            if c in splitstring[2]:
                castleavail += 2**i
        if splitstring[3] == "-":
            enpassant = -1
        else:
            square = splitstring[3]
            enpassant = -8 * (int(square[1])) + ord(square[0].upper()) - 1
        halfturn = int(splitstring[4])
        fullturn = int(splitstring[5])
        state = GameState(
            board=board,
            turn=turn,
            castleavail=castleavail,
            enpassant=enpassant,
            halfturn=halfturn,
            fullturn=fullturn,
        )
    else:
        state = GameState(board=board)

    return state


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
        piece = board[king_index + increment * i]
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

    lat_pieces = {Rank.queen, Rank.rook}
    if king_col != 7:
        if checkDirection(board, 7 - king_col, 1, king_index, lat_pieces, playerColor):
            return True

    if king_col != 0:
        if checkDirection(board, king_col, -1, king_index, lat_pieces, playerColor):
            return True

    if king_row != 7:
        if checkDirection(board, 7 - king_row, 8, king_index, lat_pieces, playerColor):
            return True

    if king_row != 0:
        if checkDirection(board, king_row, -8, king_index, lat_pieces, playerColor):
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


def isaMove(pieces: Board, moveFrom: int, moveTo: int, enpassanttarget: Optional[int]):
    piece = pieces[moveFrom]
    if piece is None:
        return False
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


def makeMove(board: Board, moveFrom: int, moveTo: int, enpassanttarget: Optional[int]):
    if isaMove(board, moveFrom, moveTo, enpassanttarget):
        board[moveTo] = board[moveFrom]
        board[moveFrom] = None
        if board[moveTo].rank == Rank.pawn and abs(moveTo - moveFrom) == 16:
            enpassanttarget = (moveFrom + moveTo) // 2
        else:
            enpassanttarget = None
    return (board, enpassanttarget)


def setup():
    classicFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    positions = [((i % 8) + 1, 8 - i // 8) for i in range(64)]
    pieces = initializeFromFEN(classicFEN)
