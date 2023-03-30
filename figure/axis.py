from matplotlib import pyplot as plt
from .coord import Length

class Axis():
    label = ""
    def __init__(self, subplot, loc="bottom"):
        self.subplot = subplot

        #mpl axis handl
        self._ax = subplot.mpl_ax
        self._fig = self._ax.figure

        if loc == "bottom":
            self.x = True
            self.mpl_axis = self._ax.get_xaxis()
        else:
            self.x = False
            self.mpl_axis = self._ax.get_yaxis()

        self.null = self.mpl_axis is None


        # init hidden vars
        self._label = ""
        self._ticks = None


    @property
    def ticks(self):
        return self._ticks

    @ticks.setter
    def ticks(self, array):
        self._ticks = array

    @property
    def lim(self):
        return self._lim

    @lim.setter
    def lim(self, l):
        if self.x:
            self._ax.set(xlim=l)
        else:
            self._ax.set(ylim=l)

        self._lim = l

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, label):
        self._label = label
        if self.x:
            self._ax.set_xlabel(label)
        else:
            self._ax.set_ylabel(label)

    def _get_bbox(self):
        #mpl transform
        rend = self._fig.canvas.get_renderer()
        trans = self._fig.dpi_scale_trans.inverted()

        #get the bbox in inches
        bbox = self.mpl_axis.get_tightbbox(rend)
        if bbox:
            tr_bbox = bbox.transformed(trans)
            return (tr_bbox.width, tr_bbox.height)
        else:
            return (0,0)


    @property
    def width(self):
        """The width of the bounding box for this axis instance"""
        if self.null:
            return Length(0)
        return Length(self._get_bbox()[0])

    @property
    def height(self):
        if self.null:
            return Length(0)
        return Length(self._get_bbox()[1])

