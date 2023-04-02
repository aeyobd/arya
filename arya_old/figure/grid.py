
class Grid:
    """
    A simple Grid class for storing and managing a 2D grid of elements.
    """

    def __init__(self, nrows=0, ncols=0, strict=False):
        """
        Initialize the Grid with the specified dimensions.

        Args:
            nrows: int, optional
                The number of rows in the grid (default: 0).
            ncols: int, optional
                The number of columns in the grid (default: 0).
            strict: bool, optional
                If True, disallow overwriting non-None elements (default: False).
        """
        self.nrows = nrows
        self.ncols = ncols
        self.strict = strict
        self.grid = [[None for _ in range(ncols)] for _ in range(nrows)]

    def __getitem__(self, position):
        """
        Get the element at the specified position (row, col).

        Args:
            position: tuple (int, int)
                A tuple (row, col) indicating the position of the element to get.

        Returns:
            The element at the specified position.
        """
        row, col = position
        return self.grid[row][col]

    def __setitem__(self, position, value):
        """
        Set the element at the specified position (row, col) to the provided value.

        Args:
            position: tuple (int, int)
                A tuple (row, col) indicating the position of the element to set.
            value: any
                The value to set at the specified position.
        """
        row, col = position
        if row >= self.nrows or col >= self.ncols:
            self.add_item(row, col, value)
        else:
            if self.strict and self.grid[row][col] is not None:
                raise ValueError(f"Element at position {position} is not None. Cannot set a new value.")
            self.grid[row][col] = value

    def __iter__(self, skip_none=True):
        """
        Iterate over the grid elements, optionally skipping None elements.

        Args:
            skip_none: bool, optional
                If True (default), skip None elements during iteration.

        Returns:
            A generator yielding tuples (row, col, element) for each element in the grid.
        """
        for row in range(self.nrows):
            for col in range(self.ncols):
                element = self.grid[row][col]
                if not (skip_none and element is None):
                    yield (row, col, element)

    def add_item(self, row, col, value):
        """
        Add a new item to the grid at the specified position, expanding the grid dimensions as necessary.

        Args:
            row: int
                The row index where the new item should be added.
            col: int
                The column index where the new item should be added.
            value: any
                The value of the new item to add.
        """
        if row >= self.nrows:
            for _ in range(row - self.nrows + 1):
                self.grid.append([None for _ in range(self.ncols)])
            self.nrows = row + 1

        if col >= self.ncols:
            for r in range(self.nrows):
                self.grid[r].extend([None for _ in range(col - self.ncols + 1)])
            self.ncols = col + 1

        self.grid[row][col] = value



