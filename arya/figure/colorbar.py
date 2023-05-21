import matplotlib as mpl
import matplotlib.pyplot as plt



class HueMap:
    def __init__(self, clim, norm):
        self._mpl = mpl.cm.ScalarMappable(
                norm=mpl.colors.Normalize(vmin=clim[0], vmax=clim[1])
                )

    def __call__(self, val):
        return self._mpl.to_rgba(val)


class Colorbar:
    def __init__(self, clim, norm="linear", **kwargs):
        self.map = HueMap(clim, norm)
        self._mpl = plt.colorbar(mappable=map, **kwargs)

    def __call__(self, val):
        return self.map(val)


