import unittest
from pyChess import initializeFromFEN


class TestFENSetup(unittest.TestCase):
    def setUp(self) -> None:
        self.pieces = initializeFromFEN(
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        )

    def testBlackRook(self):
        self.assertEqual()


# self.fenstring2 = "rnbq1bnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
# self.fenstring2 = "rnbqKbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

if __name__ == "__main__":
    unittest.main()
