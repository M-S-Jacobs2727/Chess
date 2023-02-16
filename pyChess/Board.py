import re

from pyChess import Piece, Color, Rank


class Board:
    def __init__(self, fenstring: str = "") -> None:
        self.__pieces: list[list[Piece | None]] = [
            [None for _ in range(8)] for _ in range(8)
        ]
        if fenstring != "":
            self.initializeFromFEN(fenstring)

    def __getitem__(self, pos: tuple[int, int] | str) -> Piece | None:
        if isinstance(pos, tuple):
            row, col = pos
        elif isinstance(pos, str):
            row = int(pos[1]) - 1
            col = ord(pos[0].upper()) - 65
        else:
            raise TypeError(
                f"Invalid argument type. Expected tuple of ints or str, found {type(pos)}."
            )
        try:
            return self.__pieces[row][col]
        except IndexError:
            raise ValueError(f"Invalid board position: {pos}, row {row}, column {col}.")

    def initializeFromFEN(self, fenstring: str) -> None:
        char2rank = {
            "P": Rank.pawn,
            "N": Rank.knight,
            "B": Rank.bishop,
            "R": Rank.rook,
            "Q": Rank.queen,
            "K": Rank.king,
        }
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
        for i, row in enumerate(rows):
            col = 0
            for d in row:
                if d.upper() in "PNBQRK":
                    color = Color.white if d.isupper() else Color.black
                    rank = char2rank[d.upper()]

                    self.__pieces[i][col] = Piece(rank, color)
                    col += 1
                    if d == "k":
                        numblackkings += 1
                    elif d == "K":
                        numwhitekings += 1
                elif d in "12345678":
                    col += int(d)
                else:
                    raise SyntaxError(f"Invalid character in FEN string: `{d}`")

            if col != 8:
                raise SyntaxError(
                    f"Invalid number of columns in row: {row}."
                    f" Should be 8, found {col}."
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

    def checkValidBoard(self) -> None:
        pass

    def findKing(self, color: Color) -> tuple[int, int]:
        """Can likely be sped up using `index` list method."""
        for row in range(8):
            for col in range(8):
                if self.__pieces[row][col] == Piece(Rank.king, color):
                    return row, col
        raise LookupError(f"Could not find {color.name} king.")

    def checkDirection(
        self,
        row_inc: int,
        col_inc: int,
        king_row: int,
        king_col: int,
        attackingPieces: set[Piece],
    ) -> bool:
        i = king_row + row_inc
        j = king_col + col_inc
        piece = self.__pieces[i][j]
        while piece is None and 0 <= i < 8 and 0 <= j < 8:
            i += row_inc
            j += col_inc
            piece = self.__pieces[i][j]
        if piece is None:
            return False
        return piece in attackingPieces

    def inCheck(self, playerColor: Color) -> bool:
        """Given the arrangement of `pieces`, returns `True` if the player with color
        `playerColor` is in check.
        """
        opposite_color = Color.white if playerColor == Color.black else Color.black
        king_row, king_col = self.findKing(playerColor)

        lat_pieces = {
            Piece(Rank.queen, opposite_color),
            Piece(Rank.rook, opposite_color),
        }
        if king_col != 7 and self.checkDirection(0, 1, king_row, king_col, lat_pieces):
            return True

        if king_col != 0 and self.checkDirection(0, -1, king_row, king_col, lat_pieces):
            return True

        if king_row != 7 and self.checkDirection(1, 0, king_row, king_col, lat_pieces):
            return True

        if king_row != 0 and self.checkDirection(-1, 0, king_row, king_col, lat_pieces):
            return True

        diagonal_pieces = {
            Piece(Rank.queen, opposite_color),
            Piece(Rank.bishop, opposite_color),
        }
        if playerColor == Color.black:
            diagonal_pieces.add(Piece(Rank.pawn, opposite_color))
        if (
            king_col != 7
            and king_row != 7
            and self.checkDirection(
                1,
                1,
                king_row,
                king_col,
                diagonal_pieces
                if playerColor == Color.black
                else diagonal_pieces.union({Piece(Rank.pawn, opposite_color)}),
            )
        ):
            return True

        if (
            king_col != 0
            and king_row != 7
            and self.checkDirection(
                1,
                -1,
                king_row,
                king_col,
                diagonal_pieces
                if playerColor == Color.black
                else diagonal_pieces.union({Piece(Rank.pawn, opposite_color)}),
            )
        ):
            return True

        diagonal_pieces = {
            Piece(Rank.queen, opposite_color),
            Piece(Rank.bishop, opposite_color),
        }
        if playerColor == Color.white:
            diagonal_pieces.add(Piece(Rank.pawn, opposite_color))
        if (
            king_col != 7
            and king_row != 0
            and self.checkDirection(
                -1,
                1,
                king_row,
                king_col,
                diagonal_pieces
                if playerColor == Color.white
                else diagonal_pieces.union({Piece(Rank.pawn, opposite_color)}),
            )
        ):
            return True

        if (
            king_col != 0
            and king_row != 0
            and self.checkDirection(
                -1,
                -1,
                king_row,
                king_col,
                diagonal_pieces
                if playerColor == Color.white
                else diagonal_pieces.union({Piece(Rank.pawn, opposite_color)}),
            )
        ):
            return True

        # knights
        if all(Piece(Rank.knight, opposite_color) not in row for row in self.__pieces):
            return False
        offsets = [
            (-2, -1),
            (-2, 1),
            (-1, -2),
            (-1, 2),
            (1, -2),
            (1, 2),
            (2, -1),
            (2, 1),
        ]
        col_ranges = [(1, 7), (0, 6), (2, 7), (0, 5), (2, 7), (0, 5), (1, 7), (0, 6)]
        row_ranges = [(2, 7), (2, 7), (1, 7), (1, 7), (0, 6), (0, 6), (0, 5), (0, 5)]
        for offset, col_range, row_range in zip(offsets, col_ranges, row_ranges):
            if (
                col_range[0] <= king_col <= col_range[1]
                and row_range[0] <= king_row <= row_range[1]
                and self.__pieces[king_row + offset[0]][king_col + offset[1]]
                and self.__pieces[king_row + offset[0]][king_col + offset[1]]
                == Piece(Rank.knight, opposite_color)
            ):
                return True

        return False

    def place(self, piece: Piece, row: int, col: int) -> None:
        try:
            self.__pieces[row][col] = piece
        except IndexError:
            raise IndexError(f"Invalid row ({row}) or column ({col}).")

    def remove(self, row: int, col: int) -> None:
        try:
            self.__pieces[row][col] = None
        except IndexError:
            raise IndexError(f"Invalid row ({row}) or column ({col}).")
