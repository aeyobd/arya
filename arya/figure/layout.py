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


    def add_subplot(self, subplot=None, row=None, col=None):
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
        if row is None or col is None:
            row, col = self.get_next_pos(row, col)

        if subplot is None:
            subplot = Subplot(layout=self, row=row, col=col)


        self.grid[row, col] = subplot

        return subplot

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

        for r in range(self.grid.nrows):
            for c in range(self.grid.ncols):
                if self.grid[r, c] is None:
                    return (r, c)

        # no empty spaces, create a new one
        if self.grid.ncols > self.grid.nrows:
            return (self.grid.nrows, 0)
        return (0, self.grid.ncols)

    @property
    def width(self):
        width = 0 

        for row in range(self.grid.nrows):
            x = 0 
            for col in range(self.grid.ncols):
                subplot = self.grid[row, col]
                if subplot is not None:
                    x += subplot.total_width

            width = max(width, x)
        
        return width

    @property
    def height(self):
        height = 0 

        for row in range(self.grid.nrows):
            y = 0
            for col in range(self.grid.ncols):
                subplot = self.grid[row, col]
                if subplot is not None:
                    y = max(y, subplot.total_height)
            height += y

        return height

    def update_positions(self):
        """
        Update the positions of the SubFigures in the grid.
        """
        self.mpl_fig.set_size_inches(self.width, self.height)
        y = 0

        for row in range(self.grid.nrows):
            max_height = 0
            x = 0
            
            for col in range(self.grid.ncols):
                subplot = self.grid[row, col]
                if subplot is not None:
                    subplot.position(x, y)
                    max_height = max(max_height, subplot.total_height)
                    x += subplot.total_width

            y += max_height

    def savefig(self, filename, dpi=100):
        self.create_axes()
        plt.savefig(filename, dpi=dpi)

    def show(self):
        self.update_positions()
        self.mpl_fig.show()




