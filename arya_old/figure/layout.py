import matplotlib.pyplot as plt
from .grid import Grid
from .subplot2 import Subplot

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

    def add_subfigure(self, row, col, subfigure=None):
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
        if subfigure is None:
            subfigure = SubFigure()

        self.grid[row, col] = subfigure

    def update_positions(self):
        """
        Update the positions of the SubFigures in the grid.
        """
        current_y = 0
        for position, subfigure in range(self.grid.nrows):
            max_height = 0
            current_x = 0
            for col in range(self.grid.ncols):
                subfigure = self.grid[row, col]
                if subfigure is not None:
                    subfigure.set_position_inches(current_x, current_y)
                    max_height = max(max_height, subfigure.height_inches + subfigure.padding_top + subfigure.padding_bottom)
                    current_x += subfigure.width_inches + subfigure.padding_left + subfigure.padding_right
            current_y += max_height


    def savefig(self, filename, dpi=100):
        self.create_axes()
        plt.savefig(filename, dpi=dpi)



class LayoutManager:
    def __init__(self, nrows, ncols, figsize_inches=(10, 10)):
        self.nrows = nrows
        self.ncols = ncols
        self.fig = plt.figure(figsize=figsize_inches)
        self.grid = [[None for _ in range(ncols)] for _ in range(nrows)]

    def add_subfigure(self, row, col, subfigure):
        if self.grid[row][col] is not None:
            raise ValueError(f"Cell ({row}, {col}) is already occupied.")
        self.grid[row][col] = subfigure
        self.refresh_layout()

    def refresh_layout(self):
        for row in range(self.nrows):
            for col in range(self.ncols):
                subfigure = self.grid[row][col]
                if subfigure is not None:
                    left = sum(s.total_width for s in self.grid[row][:col]) if col > 0 else 0
                    bottom = sum(s.total_height for s in reversed(self.grid[:row])) if row > 0 else 0
                    if subfigure.ax is not None:
                        subfigure.ax.set_position([left + subfigure.padding[0], bottom + subfigure.padding[3], subfigure.width, subfigure.height], which='inches')

    def create_axes(self):
        for row in range(self.nrows):
            for col in range(self.ncols):
                subfigure = self.grid[row][col]
                if subfigure is not None:
                    left = sum(s.total_width for s in self.grid[row][:col]) if col > 0 else 0
                    bottom = sum(s.total_height for s in reversed(self.grid[:row])) if row > 0 else 0
                    subfigure.create_axes(self.fig, left, bottom)

    def show(self):
        self.create_axes()
        plt.show()


    def refresh_layout(self):
        for row in range(self.nrows):
            for col in range(self.ncols):
                subfigure = self.grid[row][col]
                if subfigure is not None:
                    left_inches = sum(s.total_width for s in self.grid[row][:col]) if col > 0 else 0
                    bottom_inches = sum(s.total_height for s in reversed(self.grid[:row])) if row > 0 else 0
                    if subfigure.ax is not None:
                        subfigure.set_axes_position_inches(left_inches, bottom_inches, self.fig)

    # ... (same as before)

