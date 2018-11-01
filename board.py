class Board:
    """represents a Sudoku board of nxn dimensions."""

    def __init__(self, width=3, height=3):
        """creates a new empty sudoku board"""

        self.width = width
        self.height = height

        self.contents = []
        # Create an empty board by populating each cell with a zero.
        for i in range(self.total_dimension()):
            self.contents.append([])
            for j in range(self.total_dimension()):
                self.contents[i].append(0)

    @classmethod
    def copy(cls, other):
        retval = Board(other.width, other.height)
        for i in range(retval.total_dimension()):
            for j in range(retval.total_dimension()):
                retval.contents[i][j] = other.contents[i][j]
        return retval

    def total_dimension(self):
        """returns the size of the whole board instead of a single square."""
        return self.width * self.height

    def __str__(self):
        retval = ""
        character_width = 2 * self.height * (self.width + 1) + 1
        for i in range(self.total_dimension()):
            if i % self.height == 0:
                for k in range(character_width):
                    retval += '-'
                retval += '\n'
            for j in range(self.total_dimension()):
                if j % self.width == 0:
                    retval += '| '
                retval += str(self.contents[i][j]) + " "
            retval += '|\n'

        for k in range(character_width):
            retval += '-'
        retval += '\n'

        return retval

    def row(self, n):
        """returns all values in a given row as seen below on a 9x9 board:
        -------------------------
        | 0 0 0 | 0 0 0 | 0 0 0 |
        | 1 1 1 | 1 1 1 | 1 1 1 |
        | 2 2 2 | 2 2 2 | 2 2 2 |
        -------------------------
        | 3 3 3 | 3 3 3 | 3 3 3 |
        | 4 4 4 | 4 4 4 | 4 4 4 |
        | 5 5 5 | 5 5 5 | 5 5 5 |
        -------------------------
        | 6 6 6 | 6 6 6 | 6 6 6 |
        | 7 7 7 | 7 7 7 | 7 7 7 |
        | 8 8 8 | 8 8 8 | 8 8 8 |
        -------------------------
        """
        return self.contents[n].copy()

    def column(self, n):
        """returns all values in a given column as seen below on a 9x9 board:
        -------------------------
        | 0 1 2 | 3 4 5 | 6 7 8 |
        | 0 1 2 | 3 4 5 | 6 7 8 |
        | 0 1 2 | 3 4 5 | 6 7 8 |
        -------------------------
        | 0 1 2 | 3 4 5 | 6 7 8 |
        | 0 1 2 | 3 4 5 | 6 7 8 |
        | 0 1 2 | 3 4 5 | 6 7 8 |
        -------------------------
        | 0 1 2 | 3 4 5 | 6 7 8 |
        | 0 1 2 | 3 4 5 | 6 7 8 |
        | 0 1 2 | 3 4 5 | 6 7 8 |
        -------------------------
        """
        retval = []
        for i in range(self.total_dimension()):
            retval.append(self.contents[i][n])
        return retval

    def square(self, n):
        """returns all values in a given square indexed in row major fashion as seen below on a 9x9 board:
        -------------------------
        | 0 0 0 | 1 1 1 | 2 2 2 |
        | 0 0 0 | 1 1 1 | 2 2 2 |
        | 0 0 0 | 1 1 1 | 2 2 2 |
        -------------------------
        | 3 3 3 | 4 4 4 | 5 5 5 |
        | 3 3 3 | 4 4 4 | 5 5 5 |
        | 3 3 3 | 4 4 4 | 5 5 5 |
        -------------------------
        | 6 6 6 | 7 7 7 | 8 8 8 |
        | 6 6 6 | 7 7 7 | 8 8 8 |
        | 6 6 6 | 7 7 7 | 8 8 8 |
        -------------------------

        or on a 6x6 board (square size 3x2):
        -----------------
        | 0 0 0 | 1 1 1 |
        | 0 0 0 | 1 1 1 |
        -----------------
        | 2 2 2 | 3 3 3 |
        | 2 2 2 | 3 3 3 |
        -----------------
        | 4 4 4 | 5 5 5 |
        | 4 4 4 | 5 5 5 |
        -----------------
        """
        retval = []
        for i in range(self.height):
            for j in range(self.width):
                row = n // self.height * self.height + i
                col = (n % self.height) * self.width + j
                retval.append(self.contents[row][col])
        return retval

    def cell(self, row, column):
        """returns the value at a particular cell as would be indexed using both row and cell above."""
        return self.contents[row][column]

    def _valid_slice(self, subject):
        """determines whether or not any given list has conflicting sudoku values."""
        trimmed = [x for x in subject if x != 0]

        # This feels very expressive to me, but could increase GC pressure. Is there a pythonic 'any' function?
        out_of_bounds = [x for x in trimmed if x > self.width * self.height]
        if len(out_of_bounds) > 0:
            return False

        return len(trimmed) == len(set(trimmed))

    def valid(self):
        """determines whether or not a Sudoku board has any conflicting values."""
        for i in range(self.width * self.height):
            if not (
                    self._valid_slice(self.row(i)) and
                    self._valid_slice(self.column(i)) and
                    self._valid_slice(self.square(i))):
                return False
        return True

    def complete(self):
        """determines whether or not a Sudoku board is both `valid` and contains no empty cells."""
        if not self.valid():
            return False
        for i in range(self.width * self.height):
            for j in range(self.width * self.height):
                if self.contents[i][j] == 0:
                    return False
        return True

    def solve(self):
        if self.complete():
            return self

        if not self.valid():
            return None

        updated = Board.copy(self)
        for i in range(updated.total_dimension()):
            for j in range(updated.total_dimension()):
                if updated.contents[i][j] == 0:
                    x = i
                    y = j

        for i in range(updated.total_dimension()):
            updated.contents[x][y] = i + 1
            solved = updated.solve()
            if solved is not None:
                return solved
        return None
