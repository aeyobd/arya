from matplotlib import pyplot as plt
import numpy as np
from matplotlib.transforms import Bbox

class Legend:
    def __init__(self, loc=None, ax=None, **kwargs):

        if ax is None:
            ax = plt.gca()
        self.mpl_ax = ax

        self.mpl_leg = plt.legend(loc=loc, **kwargs)
        if loc is None:
            self.locate(loc=loc)



    @property
    def labels(self):
        return [t.get_text() for t in self.mpl_leg.texts]

    @labels.setter
    def labels(self, a):
        self._labels = a

    @property
    def handles(self):
        return self.mpl_leg.legend_handles

    @property
    def ms(self):
        return [h.get_markersize() for h in self.handles]

    @ms.setter
    def ms(self, size):
        if isinstance(size, (int, float)):
            for h in self.mpl_leg.legend_handles:
                h.set_markersize(size)
        elif isinstance(size, (tuple, list)):
            if len(size) != len(self.handles):
                raise ValueError("size must be same len as handles")
            for h in self.handles:
                h.set_markersize(size)

    def hide_handles(self):
        for h in self.handles:
            h.set_visible(False)

        self.mpl_leg.handlelength = 0
        self.mpl_leg.columnspacing = 0.8


    def color_labels(self, alpha=None):
        texts = self.mpl_leg.get_texts()
        for t, c in zip(texts, self.colors):
            t.set_color(c)


    @property
    def colors(self):
        cs = []
        for handle in self.handles:
            c = handle.get_color()
            if isinstance(c, str):
                cs.append(c)
            elif isinstance(c, (list, np.ndarray)):
                if isinstance(c[0], (int, float)):
                    cs.append(c)
                elif isinstance(c, list):
                    cs.append(c[0])
                else:
                    raise NotImplementedError
        return cs


    @colors.setter
    def colors(self, cs):
        for i in range(len(self.handles)):
            self.handles[i].set_color(cs[i])


    def create_legend(self, **kwargs):
        self.mpl_leg = self.mpl_ax.legend(
                self.handles, self.labels, frameon=False, **kwargs)


    def locate(self, loc=None):
        if loc is None:
            loc = find_best_position(self.mpl_leg)

        if isinstance(loc, str):
            loc = {
                    "upper left": 1,
                    "upper right": 2,
                    "lower left": 3,
                    "lower right": 4,
                    "outside right": -1,
                    "outside bottom": -2,
                    }[loc]

        # have to remove and recreate
        self.mpl_leg.remove()
        if loc == -1:
            self.create_legend(loc="upper left", bbox_to_anchor=(1, 1))
        elif loc == -2:
            self.create_legend(loc="upper left", bbox_to_anchor=(0, 0))
        else:
            self.create_legend(loc=loc)




def find_best_position(legend, max_bad=5):
    badnesses = [0]*4
    locs = [1,2,3,4]

    for idx, code in enumerate(locs):
        badnesses[idx] = eval_position(legend, code)

    if min(badnesses) > max_bad:
        return -1
    else:
        return locs[badnesses.index(min(badnesses))]
        


def eval_position(legend, code):
    """
    Determine the best location to place the legend.

    *consider* is a list of ``(x, y)`` pairs to consider as a potential
    lower-left corner of the legend. All are display coords.

    ===============   =============
    Location String   Location Code
    ===============   =============
    'best'            0
    'upper right'     1
    'upper left'      2
    'lower left'      3
    'lower right'     4
    'right'           5
    'center left'     6
    'center right'    7
    'lower center'    8
    'upper center'    9
    'center'          10
    ===============   =============
    """
    width = legend.get_tightbbox().width
    height = legend.get_tightbbox().height
    renderer = legend.figure._get_renderer()

    bboxes, lines, offsets = legend._auto_legend_data()

    bbox = Bbox.from_bounds(0, 0, width, height)

    l, b = legend._get_anchored_bbox(code, bbox,
                                        legend.get_bbox_to_anchor(),
                                        renderer)

    legendBox = Bbox.from_bounds(l, b, width, height)

    badness = (sum(legendBox.count_contains(line.vertices)
                   for line in lines)
               + legendBox.count_contains(offsets)
               + legendBox.count_overlaps(bboxes)
               + sum(line.intersects_bbox(legendBox, filled=False)
                     for line in lines))

    return badness
