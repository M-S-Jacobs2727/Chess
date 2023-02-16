from pyChess import Piece, Rank, Color, Board
from dataclasses import dataclass, field
from typing import Optional


@dataclass(order=True)
class GameState:
    fullturn: int = field(default=1)
    turn: Color = field(default=Color.white)
    board: Board = field(compare=False, default_factory=Board)
    castleavail: int = field(compare=False, default=15)
    enpassant: int = field(compare=False, default=-1)
    halfturn: int = field(compare=False, default=0)


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
