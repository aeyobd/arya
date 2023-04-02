import matplotlib.pyplot as plt
from ..style.style import FIG_SIZE

class Subplot:
    """
    A Subplot class that holds a Matplotlib Axes object and provides methods to
    set axis limits, labels, and control the size of the axes.
    """

    def __init__(self, figure, size=FIG_SIZE, **kwargs)
        """
        Initialize the Subplot with the given dimensions and position.

        Args:
            fig: matplotlib.figure.Figure
                The Matplotlib Figure instance the subplot belongs to.
            x_inches: float
                The x position of the subplot in inches.
            y_inches: float
                The y position of the subplot in inches.
            width_inches: float
                The width of the subplot in inches.
            height_inches: float
                The height of the subplot in inches.
        """
        self.fig = figure
        self.mpl_ax = self.fig.mpl_fig.add_axes([0,0,1,1])

        self.fig.add_subplot(self)

        self.width = size[0]
        self.height = size[1]

        self.set(**kwargs)


    @property
    def xlim(self):
        return self.mpl_ax.get_xlim()

    @xlim.setter
    def xlim(self, value):
        self.mpl_ax.set_xlim(value)

    @property
    def ylim(self):
        return self.mpl_ax.get_ylim()

    @ylim.setter
    def ylim(self, value):
        self.mpl_ax.set_ylim(value)

    @property
    def xlabel(self):
        return self.mpl_ax.get_xlabel()

    @xlabel.setter
    def xlabel(self, value):
        self.mpl_ax.set_xlabel(value)

    @property
    def ylabel(self):
        return self.mpl_ax.get_ylabel()

    @ylabel.setter
    def ylabel(self, value):
        self.mpl_ax.set_ylabel(value)

    def set(self, **kwargs):
        """
        Set multiple attributes of the subplot using keyword arguments.

        Parameters
        ----------
        **kwargs: keyword arguments
            The attributes to set and their corresponding values.

        Returns
        -------
        self: Subplot
            The current subplot instance (for chaining)
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"Invalid attribute '{key}' for Subplot.")

