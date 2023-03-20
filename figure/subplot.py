from matplotlib import pyplot as plt
from .coord import Length
from .axis import Axis
from itertools import cycle
from ..style.style import COLORS, MARKERS, FILL, FIG_SIZE

class Subplot():
    def __init__(self, figure=None, size=FIG_SIZE, loc="right", row=0, col=0, ax=None, add_to_fig = True):
        if figure is None:
            from .figure import Figure
            figure = Figure()

        self.figure = figure

        if ax is None:
            self.mpl_ax = self.figure.mpl_fig.add_subplot()
        else:
            self.mpl_ax = ax

        self._v_pad = None
        self._h_pad = None

        self.x = Axis(self, "bottom")
        self.y = Axis(self, "left")
        self.width = size[0]
        self.height = size[1]

        self.row = row
        self.col = col
        if add_to_fig:
            self.figure.add_subplot(subplot=self, row=row, col=col)
        self._layers = []

        self.lc_cycle = cycle(COLORS)
        self.mc_cycle = cycle(COLORS)
        self.ms_cycle = cycle(MARKERS)



    def next_linesty(self):
        return next(self.lc_cycle)

    def next_marksty(self):
        return next(self.mc_cycle), next(self.ms_cycle)

    def locate(self, row, col):
        self.mpl_ax.set_axes_locator(self.figure.mpl_div.new_locator(nx=row, ny=col))

    def add_legend(self, legend):
        self.legend = legend

    def remove(self):
        self.mpl_ax.remove()

    def add_layer(self, layer):
        self._layers.append(layer)

    def save(self, filename):
        self.figure.save(filename)

    def show(self):
        self.figure.show()

    @property
    def layers(self):
        return self._layers

    @property
    def labels(self):
        return [lay.label for lay in self.layers]

    @property
    def handles(self):
        return [lay.handle for lay in self.layers]

    @property
    def figure(self):
        """ The Figure object associated with this subplot """
        return self._figure

    @figure.setter
    def figure(self, value):
        self._figure = value

    @property
    def width(self):
        """ The width of this subplot, as a Length """ 
        return self._width

    @property
    def height(self):
        return self._height

    @width.setter
    def width(self, w):
        self._width = Length(w)

    @height.setter
    def height(self, h):
        self._height = Length(h)

    @property
    def h_pad(self):
        """A duple of Length representing padding to the left
        and right of the subplot
        """
        if self._h_pad is None:
            return (self.y.width, Length(0))
        else:
            return self._h_pad

    @property
    def v_pad(self):
        """A duple of Length representing padding to the bottom
        and top of the subplot (respectively)
        """
        if self._v_pad is None:
            return (self.x.height, Length(0))
        else:
            return self._v_pad

    @v_pad.setter
    def v_pad(self, a):
        self._v_pad = a

    @h_pad.setter
    def h_pad(self, a):
        self._h_pad = a

    @property
    def title(self):
        return self._title

