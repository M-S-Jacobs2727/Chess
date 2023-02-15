import unittest
import pyChess
from pyChess import Rank, Color


class TestInCheck(unittest.TestCase):
    def setUp(self) -> None:
        self.pieces = [None for _ in range(64)]

    def testInCheckRook1(self):
        self.pieces[0] = pyChess.Piece(Rank.king, Color.white)
        self.pieces[35] = pyChess.Piece(Rank.king, Color.black)
        self.pieces[33] = pyChess.Piece(Rank.rook, Color.white)
        self.assertTrue(
            pyChess.inCheck(self.pieces, Color.black),
            "Black king should be in check by rook",
        )

    def testInCheckRook2(self):
        self.pieces[0] = pyChess.Piece(Rank.king, Color.white)
        self.pieces[35] = pyChess.Piece(Rank.king, Color.black)
        self.pieces[43] = pyChess.Piece(Rank.rook, Color.white)
        self.assertTrue(
            pyChess.inCheck(self.pieces, Color.black),
            "Black king should be in check by rook",
        )

    def testInCheckRook3(self):
        self.pieces[0] = pyChess.Piece(Rank.king, Color.white)
        self.pieces[35] = pyChess.Piece(Rank.king, Color.black)
        self.pieces[59] = pyChess.Piece(Rank.rook, Color.white)
        self.assertTrue(
            pyChess.inCheck(self.pieces, Color.black),
            "Black king should be in check by rook",
        )

    def testInCheckRook4(self):
        self.pieces[0] = pyChess.Piece(Rank.king, Color.white)
        self.pieces[35] = pyChess.Piece(Rank.king, Color.black)
        self.pieces[39] = pyChess.Piece(Rank.rook, Color.white)
        self.assertTrue(
            pyChess.inCheck(self.pieces, Color.black),
            "Black king should be in check by rook",
        )

    def testNotInCheckRook1(self):
        self.pieces[0] = pyChess.Piece(Rank.king, Color.white)
        self.pieces[35] = pyChess.Piece(Rank.king, Color.black)
        self.pieces[31] = pyChess.Piece(Rank.rook, Color.white)
        self.assertFalse(
            pyChess.inCheck(self.pieces, Color.black),
            "Black king is in check from previous row",
        )

    def testNotInCheckRook2(self):
        self.pieces[0] = pyChess.Piece(Rank.king, Color.white)
        self.pieces[35] = pyChess.Piece(Rank.king, Color.black)
        self.pieces[39] = pyChess.Piece(Rank.rook, Color.white)
        self.assertFalse(
            pyChess.inCheck(self.pieces, Color.white),
            "White king is in check from nothing",
        )

    def testNotInCheckRook3(self):
        self.pieces[37] = pyChess.Piece(Rank.king, Color.white)
        self.pieces[35] = pyChess.Piece(Rank.king, Color.black)
        self.pieces[39] = pyChess.Piece(Rank.rook, Color.white)
        self.assertFalse(
            pyChess.inCheck(self.pieces, Color.black),
            "Black king is in check from blocked rook",
        )

    def testNotInCheckRook4(self):
        self.pieces[19] = pyChess.Piece(Rank.king, Color.white)
        self.pieces[35] = pyChess.Piece(Rank.king, Color.black)
        self.pieces[3] = pyChess.Piece(Rank.rook, Color.white)
        self.assertFalse(
            pyChess.inCheck(self.pieces, Color.white),
            "Black king is in check from blocked rook",
        )

    def testNotInCheckRook5(self):
        self.pieces[0] = pyChess.Piece(Rank.king, Color.white)
        self.pieces[35] = pyChess.Piece(Rank.king, Color.black)
        self.pieces[45] = pyChess.Piece(Rank.rook, Color.white)
        self.assertFalse(
            pyChess.inCheck(self.pieces, Color.white),
            "Black king is in check from rook a knight's move away",
        )


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
