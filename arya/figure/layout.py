import matplotlib.pyplot as plt
from .grid import Grid
from .subplot import Subplot

class LayoutManager:
    """
    A simple LayoutManager class for arranging SubFigures in a grid layout.
    """

    def __init__(self, nrows=1, ncols=1, padding=0.2):
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
        self.padding = [padding] * 4

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


    def _calc_dims(self, align='both'):
        if align not in ('row', 'column', 'both'):
            raise ValueError("Invalid align value. Must be 'row', 'column', or 'both'.")

        row_paddings = [0] * self.grid.nrows
        col_paddings = [0] * self.grid.ncols

        if align in ('row', 'both'):
            for row in range(self.grid.nrows):
                max_padding = [0, 0, 0, 0]
                for col in range(self.grid.ncols):
                    subplot = self.grid[row, col]
                    if subplot is not None:
                        max_padding = [max(a, b) for a, b in zip(max_padding, subplot.padding)]
                row_paddings[row] = max_padding

        if align in ('column', 'both'):
            for col in range(self.grid.ncols):
                max_padding = [0, 0, 0, 0]
                for row in range(self.grid.nrows):
                    subplot = self.grid[row, col]
                    if subplot is not None:
                        max_padding = [max(a, b) for a, b in zip(max_padding, subplot.padding)]
                col_paddings[col] = max_padding

        y = self.padding[1]
        for row in range(self.grid.nrows):
            max_height = 0
            x = self.padding[0]

            for col in range(self.grid.ncols):
                subplot = self.grid[row, col]
                if subplot is not None:
                    x_padding, y_padding = row_paddings[row][0], col_paddings[col][1]
                    
                    max_height = max(max_height, subplot.height)
                    x += subplot.width + row_paddings[row][2] + row_paddings[row][0]

            y += max_height + col_paddings[row][1] + col_paddings[row][3]

        total_width = x + self.padding[2]
        total_height = y + self.padding[3]

        self.width = total_width
        self.height = total_height

        return row_paddings, col_paddings, total_width, total_height


    def update_positions(self, align='both'):
        """
        Update the positions of the SubFigures in the grid.
        
        Parameters
        ----------
        align: str, optional
            Alignment for padding calculation. 'row', 'column', or 'both'.
        """

        if align not in ('row', 'column', 'both'):
            raise ValueError("Invalid align value. Must be 'row', 'column', or 'both'.")


        # calculates the needed paddings
        row_paddings, col_paddings, width, height = self._calc_dims(align)
        self.mpl_fig.set_size_inches(width, height)

        y = height
        for row in range(self.grid.nrows):
            max_height = 0
            x = self.padding[0]
            
            for col in range(self.grid.ncols):
                subplot = self.grid[row, col]
                if subplot is not None:
                    x_padding, y_padding = row_paddings[row][0], col_paddings[col][3]
                    subplot.position(x + x_padding, y - y_padding - subplot.height)
                    
                    max_height = max(max_height, subplot.height)
                    x += subplot.width + row_paddings[row][0] + row_paddings[row][2]

            y -= max_height + col_paddings[row][1] + col_paddings[row][3]


    def savefig(self, filename, dpi=100):
        self.create_axes()
        plt.savefig(filename, dpi=dpi)


    def show(self):
        self.update_positions()
        self.mpl_fig.show()

