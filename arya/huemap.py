import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np



class HueMap:
    def __init__(self, clim, norm="linear", cmap=None):
        if cmap is None:
            cmap = plt.get_cmap()


        if isinstance(norm, (tuple, list, np.ndarray)):
            xs = 0.5*(norm[1:] + norm[: -1])
            colors = cmap((xs-clim[0])/(clim[1] - clim[0]))
            cmap = mpl.colors.ListedColormap(colors)
            norm = mpl.colors.BoundaryNorm(norm, len(norm) - 1)
            
        elif norm == "linear":
            norm = mpl.colors.Normalize(vmin=clim[0], vmax=clim[1])
        elif norm == "log":
            norm = mpl.colors.LogNorm(vmin=clim[0], vmax=clim[1])

        self._mpl = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)

    def __call__(self, val):
        return self._mpl.to_rgba(val)
    
    