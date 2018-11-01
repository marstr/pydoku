import unittest

import board


class TestBoard(unittest.TestCase):
    def test_cell(self):
        subject = board.Board()
        subject.contents[0][1] = 6
        subject.contents[2][2] = 9
        subject.contents[3][3] = 1
        self.assertEqual(0, subject.cell(0, 0))
        self.assertEqual(6, subject.cell(0, 1))
        self.assertEqual(9, subject.cell(2, 2))
        self.assertEqual(1, subject.cell(3, 3))

    def test_row(self):
        subject = board.Board(2, 2)
        subject.contents[0] = [1, 2, 0, 0]
        self.assertEqual([1, 2, 0, 0], subject.row(0))
        self.assertEqual([0, 0, 0, 0], subject.row(1))

    def test_column(self):
        subject = board.Board(2, 2)
        subject.contents[0][0] = 1
        subject.contents[1][0] = 2
        subject.contents[2][0] = 3
        subject.contents[3][0] = 4
        self.assertEqual([1, 2, 3, 4], subject.column(0))
        self.assertEqual([0, 0, 0, 0], subject.column(1))
        self.assertEqual([0, 0, 0, 0], subject.column(2))

    def test_square(self):
        subject = board.Board(3, 2)
        subject.contents[0] = [1, 2, 3, 4, 5, 6]
        subject.contents[1] = [4, 5, 6, 1, 2, 3]
        subject.contents[2] = [2, 3, 4, 5, 6, 1]
        subject.contents[3] = [5, 6, 1, 2, 3, 4]
        subject.contents[4] = [3, 4, 5, 6, 1, 2]
        subject.contents[5] = [6, 1, 2, 3, 4, 5]

        self.assertEqual([1, 2, 3, 4, 5, 6], subject.square(0), "square 0")
        self.assertEqual([4, 5, 6, 1, 2, 3], subject.square(1), "square 1")
        self.assertEqual([2, 3, 4, 5, 6, 1], subject.square(2), "square 2")
        self.assertEqual([5, 6, 1, 2, 3, 4], subject.square(3), "square 3")
        self.assertEqual([3, 4, 5, 6, 1, 2], subject.square(4), "square 4")
        self.assertEqual([6, 1, 2, 3, 4, 5], subject.square(5), "square 5")

    def test_valid(self):
        dups = board.Board(2, 2)
        dups.contents[0][0] = 1
        dups.contents[0][1] = 1
        self.assertFalse(dups.valid(), "didn't find expected duplicates in row")

        dups = board.Board(2, 2)
        dups.contents[0][0] = 1
        dups.contents[1][0] = 1
        self.assertFalse(dups.valid(), "didn't find expected duplicates in column")

        dups = board.Board(2, 2)
        dups.contents[2][2] = 1
        dups.contents[3][3] = 1
        self.assertFalse(dups.valid(), "didn't find expected duplicates in square")

        self.assertTrue(board.Board().valid(), "empty default board is not considered valid")

    def test_complete(self):
        subject = board.Board(3, 2)
        subject.contents[0] = [1, 2, 3, 4, 5, 6]
        subject.contents[1] = [4, 5, 6, 1, 2, 3]
        subject.contents[2] = [2, 3, 4, 5, 6, 1]
        subject.contents[3] = [5, 6, 1, 2, 3, 4]
        subject.contents[4] = [3, 4, 5, 6, 1, 2]
        subject.contents[5] = [6, 1, 2, 3, 4, 5]

        self.assertTrue(subject.complete(), "complete board reported as incomplete")

        subject.contents[5][5] = 0
        self.assertFalse(subject.complete(), "incomplete board reported as complete")

        subject.contents[5][5] = 4
        self.assertFalse(subject.complete(), "invalid board reported as complete")

    def test_solve(self):
        subject_small = board.Board(2, 2)
        subject_small.contents[0] = [1, 2, 3, 4]
        subject_small.contents[1] = [3, 4, 1, 2]
        subject_small.contents[2] = [2, 3, 4, 1]

        solved = subject_small.solve()
        self.assertEqual([1, 2, 3, 4], solved.contents[0], "small row 0")
        self.assertEqual([3, 4, 1, 2], solved.contents[1], "small row 1")
        self.assertEqual([2, 3, 4, 1], solved.contents[2], "small row 2")
        self.assertEqual([4, 1, 2, 3], solved.contents[3], "small row 3")

        empty = board.Board()
        solved = empty.solve()
        self.assertIsNotNone(solved, "no solution found for empty board")
        self.assertTrue(solved.complete(), "reported solution is incomplete")