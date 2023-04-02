import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
from ..style.style import FIG_SIZE

class SubPlot:
    def __init__(self, plot=None, size=FIG_SIZE, figure=None,
                 padding=(0.1, 0.1, 0.1, 0.1)):
        if figure is None:
            pass

        self.plot_instance = None
        self.width = size[0]
        self.height = size[1]
        self.padding = padding  # (left, right, top, bottom)


    @property
    def total_width(self):
        return self.width + self.padding[0] + self.padding[1]

    @property
    def total_height(self):
        return self.height + self.padding[2] + self.padding[3]

    def create_axes(self, fig, left, bottom):
        self.ax = fig.add_axes([left + self.padding[0], bottom + self.padding[3], 
                                self.width, self.height])
        self.plot_instance.plot(self.ax)
        return self.ax

    def set_padding(self, left=None, right=None, top=None, bottom=None):
        left = left if left is not None else self.padding[0]
        right = right if right is not None else self.padding[1]
        top = top if top is not None else self.padding[2]
        bottom = bottom if bottom is not None else self.padding[3]
        self.padding = (left, right, top, bottom)

    def set_axes_position_inches(self, left_inches, bottom_inches, fig):
        if self.mpl_ax is None:
            raise ValueError("Axes have not been created. Call create_axes() first.")
        
        # Convert inches to figure coordinates
        bbox_inches = Bbox.from_bounds(left_inches, bottom_inches, self.width, self.height)
        bbox_fig = fig.transFigure.inverted().transform_bbox(bbox_inches)
        
        self.ax.set_position(bbox_fig)

