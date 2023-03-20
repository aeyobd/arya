from matplotlib import pyplot as plt

class Legend:
    def __init__(self, subplot):
        self.labels = subplot.labels

        self.mpl_leg = subplot.mpl_ax.legend(subplot.handles, self.labels, frameon=False)
        subplot.add_legend(self)

    @property
    def labels(self):
        return self._labels

    @labels.setter
    def labels(self, a):
        self._labels = a

    @property
    def handles(self):
        return self.mpl_leg.legendHandles

    @property
    def ms(self):
        return [h.get_markersize() for h in self.handles]

    @ms.setter
    def ms(self, size):
        if isinstance(size, (int, float)):
            for h in self.mpl_leg.legendHandles:
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
        self.mpl_leg.columnspacing = 0

    def color_labels(self, alpha=None):
        texts = self.mpl_leg.get_texts()
        for t, c in zip(texts, self.colors):
            t.set_color(c)

    @property
    def colors(self):
        if len(self.handles[0].get_color()) != 4:
            return [h.get_color()[0] for h in self.handles]
        else:
            return [h.get_color() for h in self.handles]

    @colors.setter
    def colors(self, cs):
        for i in range(len(self.handles)):
            self.handles[i].set_color(cs[i])


