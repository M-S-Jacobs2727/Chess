import unittest
import pyChess
from pyChess import Rank, Color


class TestFENSetup(unittest.TestCase):
    def setUp(self) -> None:
        self.pieces = pyChess.initializeFromFEN(
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        )

    def testBlackRook(self):
        self.assertEqual(self.pieces[0], pyChess.Piece(Rank.rook, Color.black))

    def testBlackKnight(self):
        self.assertEqual(self.pieces[6], pyChess.Piece(Rank.knight, Color.black))

    def testBlackBishop(self):
        self.assertEqual(self.pieces[2], pyChess.Piece(Rank.bishop, Color.black))

    def testBlackQueen(self):
        self.assertEqual(self.pieces[3], pyChess.Piece(Rank.queen, Color.black))

    def testBlackKing(self):
        self.assertEqual(self.pieces[4], pyChess.Piece(Rank.king, Color.black))

    def testBlackPawn(self):
        self.assertEqual(self.pieces[12], pyChess.Piece(Rank.pawn, Color.black))

    def testWhiteRook(self):
        self.assertEqual(self.pieces[63], pyChess.Piece(Rank.rook, Color.white))

    def testWhiteKnight(self):
        self.assertEqual(self.pieces[57], pyChess.Piece(Rank.knight, Color.white))

    def testWhiteBishop(self):
        self.assertEqual(self.pieces[61], pyChess.Piece(Rank.bishop, Color.white))

    def testWhiteQueen(self):
        self.assertEqual(self.pieces[59], pyChess.Piece(Rank.queen, Color.white))

    def testWhiteKing(self):
        self.assertEqual(self.pieces[60], pyChess.Piece(Rank.king, Color.white))

    def testWhitePawn(self):
        self.assertEqual(self.pieces[50], pyChess.Piece(Rank.pawn, Color.white))

    def testEmptySquare(self):
        self.assertIsNone(self.pieces[20])



# self.fenstring2 = "rnbq1bnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
# self.fenstring2 = "rnbqKbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

if __name__ == "__main__":
    unittest.main()
