import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
from ..style.style import FIG_SIZE


class Subplot:
    """
    A Subplot class that holds a Matplotlib Axes object and provides methods to
    set axis limits, labels, and control the size of the axes.
    """

    def __init__(self, layout=None, size=FIG_SIZE, row=None, col=None, 
                 padding=0.1, **kwargs):
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
        if layout is None:
            from .layout import LayoutManager
            layout = LayoutManager()

        self.layout = layout

        self.mpl_fig = self.layout.mpl_fig
        self.mpl_ax = self.mpl_fig.add_axes([0,0,1,1])

        self.layout.add_subplot(self, row=row, col=col)

        self.width = size[0]
        self.height = size[1]
        
        self._padding = [padding] * 4

        self.set(**kwargs)

    def position(self, x, y, width=None, height=None):
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height

        if self.mpl_ax is None:
            raise ValueError("Axes have not been created. Call create_axes() first.")
        
        # Convert inches to figure coordinates
        bbox_in = Bbox.from_bounds(x, y, self.width, self.height)
        bbox_fig = bbox_in.transformed(self.layout.mpl_fig.dpi_scale_trans)
        bbox_fig = bbox_fig.transformed(self.layout.mpl_fig.transFigure.inverted())
        
        self.mpl_ax.set_position(bbox_fig)



    @property
    def total_width(self):
        return self.width + self.padding[0] + self.padding[2]

    @property
    def total_height(self):
        return self.height + self.padding[1] + self.padding[3]

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


    def __str__(self):
        return f"<subplot {self.width}x{self.height}in>"

    def __repr__(self):
        return str(self)

    def _get_bbox(self, ax):
        rend = self.mpl_fig.canvas.get_renderer()
        trans = self.mpl_fig.dpi_scale_trans.inverted()
        bbox = ax.get_tightbbox(rend)

        if bbox:
            tr_bbox = bbox.transformed(trans)
            return (tr_bbox.width, tr_bbox.height)
        return (0, 0)


    @property
    def ax_width(self):
        ax = self.mpl_ax.get_yaxis()
        box = self._get_bbox(ax)
        return box[0]

    @property
    def ax_height(self):
        ax = self.mpl_ax.get_xaxis()
        box = self._get_bbox(ax)
        return box[1]

    @property
    def padding(self):
        pad = self._padding.copy()
        pad[0] += self.ax_width
        pad[1] += self.ax_height
        return pad
        











