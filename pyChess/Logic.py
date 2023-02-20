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


def isaMove(
    board: Board,
    playerColor: Color,
    from_row: int,
    from_col: int,
    to_row: int,
    to_col: int,
    enpassanttarget: tuple[int, int] | None,
    castleavail: int,
):
    """Performs multiple checks to ensure that the desired move is valid and legal.
    This starts with preliminary checks for any piece:
    * Both squares are in the bounds of the board
    * The 'from' square contains a piece of the player's color
    * The 'to' square does not contain a piece of the same color
    * The move does not put the player's king in check

    Then, the move is checked against the piece type:
    * For knights, we only need to check that the move is two in one direction and one
      in the other
    * For rooks, bishops, and queens, we check that the move is in a valid direction
      and doesn't jump over any pieces
    * For the king, we check against castling availability, rows and columns moved is
      <=1, and that the 'to' square doesn't neighbor a king (which isn't covered under
       `inCheck`)
    * For pawns, the only legal moves are forward in the valid direction, based on
      color, then 1 forward if there is no piece there, 1 diagonally if there is a
      piece there, and two forward if there are no pieces in either square and the
      'from' square is either the 2nd or 7th rank.
    """
    piece = board[from_row][from_col]
    if piece is None:
        return False
    if piece.color != playerColor:
        return False
    to_square = board[to_row][to_col]
    if to_square and to_square.color == playerColor:
        return False

    # Check if move puts king in check
    board.place(piece, to_row, to_col)
    board.remove(from_row, from_col)
    is_bad = board.inCheck(playerColor)
    board.place(piece, from_row, from_col)
    board.remove(to_row, to_col)
    if is_bad:
        return False

    if piece.rank == Rank.knight:
        return (abs(to_row - from_row), abs(to_col - from_col)) in [(1, 2), (2, 1)]
    elif piece.rank == Rank.king:
        # check for neighboring King
        enemy_king_row, enemy_king_col = board.findKing(
            Color.black if playerColor == Color.white else Color.white
        )
        if abs(to_row - enemy_king_row) <= 1 and abs(to_col - enemy_king_col) <= 1:
            return False
        # check for castling
        if playerColor == Color.white and from_row == to_row == 7 and from_col == 4 and (to_col == 2 or to_col == 6):
            if "Q" in castleavail and to_col == 2 and board[7][3] is None and board[7][2] is None and board[7][1] is None:
                board.place(piece, 7, 3)
                board.remove(7, 4)
                is_bad = board.inCheck(playerColor)
                board.place(piece, 7, 4)
                board.remove(7, 3)
                return (not is_bad)
            elif "K" in castleavail and to_col == 6 and board[7][5] is None and board[7][6] is None:
                board.place(piece, 7, 5)
                board.remove(7, 4)
                is_bad = board.inCheck(playerColor)
                board.place(piece, 7, 4)
                board.remove(7, 5)
                return (not is_bad)
            else:
                return False
        elif playerColor == Color.black and from_row == to_row == 1 and from_col == 4 and (to_col == 2 or to_col == 6):
            if "q" in castleavail and to_col == 2 and board[7][3] is None and board[7][2] is None and board[7][1] is None:
                board.place(piece, 7, 3)
                board.remove(7, 4)
                is_bad = board.inCheck(playerColor)
                board.place(piece, 7, 4)
                board.remove(7, 3)
                return (not is_bad)
            elif "k" in castleavail and to_col == 6 and board[7][5] is None and board[7][6] is None:
                board.place(piece, 7, 5)
                board.remove(7, 4)
                is_bad = board.inCheck(playerColor)
                board.place(piece, 7, 4)
                board.remove(7, 5)
                return (not is_bad)
            else:
                return False
        # check for moving 1 square in each direction
        if abs(from_row - to_row) > 1 or abs(from_col - to_col) > 1:
            return False
    elif piece.rank == Rank.rook:
        if from_row != to_row and from_col != to_col:
            return False
        if (
            (
                from_row == to_row
                and from_col < to_col
                and any(board[from_row][from_col + 1 : to_col - 1])
            )
            or (from_row == to_row and any(board[from_row][to_col + 1 : from_col - 1]))
            or (
                from_row < to_row
                and any(row[from_col] for row in board[from_row + 1 : to_row - 1])
            )
            or (any(row[from_col] for row in board[to_row + 1 : from_row - 1]))
        ):
            return False
    elif piece.rank == Rank.bishop:
        nsquares = abs(to_row - from_row)
        if nsquares != abs(to_col - from_col):
            return False
        row_inc = (to_row - from_row) / nsquares
        col_inc = (to_col - from_col) / nsquares
        if any(
            board[from_row + row_inc * i][from_col + col_inc * i]
            for i in range(1, nsquares)
        ):
            return False
    elif piece.rank == Rank.queen:
        if abs(to_row - from_row) == abs(to_col - from_col):  # diagonal movement
            nsquares = abs(to_row - from_row)
            row_inc = (to_row - from_row) / nsquares
            col_inc = (to_col - from_col) / nsquares
            if any(
                board[from_row + row_inc * i][from_col + col_inc * i]
                for i in range(1, nsquares)
            ):
                return False
        elif (from_row == to_row) == (from_col == to_col):  # non-lateral movement
            return False
        if (  # lateral movement
            (
                from_row == to_row
                and from_col < to_col
                and any(board[from_row][from_col + 1 : to_col - 1])
            )
            or (from_row == to_row and any(board[from_row][to_col + 1 : from_col - 1]))
            or (
                from_row < to_row
                and any(row[from_col] for row in board[from_row + 1 : to_row - 1])
            )
            or (any(row[from_col] for row in board[to_row + 1 : from_row - 1]))
        ):
            return False
    else:  # pawn, most complicated...
        if (
            playerColor == Color.white
            and from_col == to_col
            and from_row - 1 == to_row
            and board[to_row][to_col] is None
        ):
            return True
        if (
            playerColor == Color.black
            and from_col == to_col
            and from_row + 1 == to_row
            and board[to_row][to_col] is None
        ):
            return True
        if (
            playerColor == Color.white
            and abs(from_col - to_col) == 1
            and from_row - 1 == to_row
            and (
                board[to_row][to_col]
                or (enpassanttarget and enpassanttarget == (to_row, to_col))
            )
        ):
            return True
        if (
            playerColor == Color.black
            and abs(from_col - to_col) == 1
            and from_row + 1 == to_row
            and (
                board[to_row][to_col]
                or (enpassanttarget and enpassanttarget == (to_row, to_col))
            )
        ):
            return True
        if (
            playerColor == Color.white
            and from_row == 6
            and to_row == 4
            and from_col == to_col
            and board[5][from_col] is None
            and board[4][from_col] is None
        ):
            return True
        if (
            playerColor == Color.black
            and from_row == 1
            and to_row == 3
            and from_col == to_col
            and board[2][from_col] is None
            and board[3][from_col] is None
        ):
            return True
        return False

    return True


def makeMove(
    board: Board,
    from_row: int,
    from_col: int,
    to_row: int,
    to_col: int,
    enpassanttarget: tuple[int, int] | None,
):
    if not isaMove(board, from_row, from_col, to_row, to_col, enpassanttarget):
        return (board, enpassanttarget)
    piece = board[from_row][from_col]
    board[to_row][to_col] = piece
    board[from_row][from_col] = None
    if piece.rank == Rank.pawn and abs(to_row - from_row) == 2:
        enpassanttarget = (to_row + from_row) // 2
    else:
        enpassanttarget = None
    return (board, enpassanttarget)


def setup():
    classicFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = Board(classicFEN)
