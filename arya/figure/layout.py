import matplotlib.pyplot as plt
from .grid import Grid
from .subplot import Subplot

class LayoutManager:
    """
    A simple LayoutManager class for arranging SubFigures in a grid layout.
    """

    def __init__(self, nrows=1, ncols=1):
        """
        Initialize the LayoutManager with the specified dimensions.

        Parameters
        ----------
        nrows: int, (default: 1)
            The number of rows in the grid layout.
        ncols: int, (default: 1)
            The number of columns in the grid layout.
        """
        self.grid = Grid(nrows, ncols)

        self.mpl_fig = plt.figure()

    def add_subplot(self, subplot=None, row=0, col=0):
        """
        Add a SubFigure instance to the grid at the specified position.

        Parameters
        ----------
        row: int
            The row index where the SubFigure should be added.
        col: int
            The column index where the SubFigure should be added.
        subfigure: SubFigure, optional
            The SubFigure instance to add to the grid.
        """
        if subplot is None:
            subplot = Subplot(layout=self)

        self.grid[row, col] = subplot

    def get_next_pos(self, row=None, col=None) -> tuple[int]:
        """
        Gets the next available position with optional row and col spec

        Parameters
        ----------
        row: int, optional
            The row to find a position
        col: int, optional
            The column to find a position

        Returns:
        -------
        (row:int, col:int)
            The row and column suggestion
        """
        if row is not None:
            if col is not None:
                return (row, col)

            for i in range(self.grid.ncols):
                if self.grid[row, i] is None:
                    return (row, i)
            return (row, self.grid.ncols)

        if col is not None:
            for i in range(self.grid.nrows):
                if self.grid[i, col] is None:
                    return (i, col)

            return (self.grid.nrows, col)

        for pos, child in self.grid:
            if child is None:
                return pos

        # no empty spaces, create a new one
        if self.grid.nrows > self.grid.ncols:
            return (self.grid.nrows, 0)
        return (self.grid.ncols)


    def update_positions(self):
        """
        Update the positions of the SubFigures in the grid.
        """
        y = 0
        for position, subfigure in range(self.grid.nrows):
            max_height = 0
            x = 0
            for col in range(self.grid.ncols):
                subplot = self.grid[row, col]
                if subplot is not None:
                    subplot.position(x, y)
                    max_height = max(max_height, subplot.total_height)
                    current_x += subplot.total_width

            current_y += max_height


    def savefig(self, filename, dpi=100):
        self.create_axes()
        plt.savefig(filename, dpi=dpi)



